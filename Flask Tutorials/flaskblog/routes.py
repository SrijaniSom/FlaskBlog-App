# import requests
from flaskblog.models import User, Post
from flask import render_template,flash,redirect, session,url_for,request,abort
from flaskblog.form import RegistrationForm, LoginForm, AccountUpdateForm, PostForm,RequestResetPasswordForm,ResetPasswordForm
from flaskblog import app, db, bcrypt,mail
from flask_login import login_user, current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

# posts=[{
#     'author':'Richard Zone',
#     'title':'Blog Post 1',
#     'content_type':'This is the first blog to be uploaded!',
#     'date_posted':'19.05.2024'
# },{
#     'author':'Tommy Hillary',
#     'title':'Blog Post 2',
#     'content_type':'This is the second blog to be uploaded!',
#     'date_posted':'20.05.2024'

# }]



@app.route("/")
def hello():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('home.html',posts=posts,)

@app.route("/about")
def about():
    return render_template('about.html',title='About Us')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
    

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    
    form=RegistrationForm()

    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, password=hashed_pw,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        print('successful!')
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    else:
        print(' not successful!')
    return render_template('register.html', title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello'))
        else:
            flash('Your login credentials are invalid! Please check again!','danger')
        
    return render_template('login.html', title='Login',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('hello'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form=AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
            
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your Account Details Are Updated','success')
        return redirect(url_for('account'))
    
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    
    
    image_file=url_for('static',filename='profile_pics/'+ current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post is Updated!','success')
        return redirect(url_for('hello'))
    
    return render_template('create_post.html', title = 'Create New Post', form=form,legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if(current_user != post.author):
        abort(403)
    
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your Post Has Been Updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content

    return render_template('create_post.html',title="Update Post",form=form,legend='Update Post')

@app.route("/delete_post/<int:post_id>",methods=['GET','POST'])
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if(current_user != post.author):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('hello'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    print(user)
    print(username)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_email(user):
    token=user.get_reset_token()
    print("token here",token)
    msg=Message('Password Reset Sent',recipients=[user.email],sender='sujatasom79@gmail.com')
    msg.body=f'''To reset your password, visit the following link:
    {url_for('reset_password', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    print(msg)

@app.route("/reset_password",methods=['GET','POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    
    form=RequestResetPasswordForm()
    if form.validate_on_submit():
        print("i am reaching here")
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent!','warning')
        return redirect(url_for('login'))

    return render_template('reset_requests.html',title='Reset Password',form=form)

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    user=User.verify_token(token)
    if user is None:
        flash('Your token is invalid or expired!','warning')
        return redirect(url_for('request_reset'))
    print("user here",user)
    form=ResetPasswordForm()
    print(form)
    if form.validate_on_submit():
        print("reset form is validated")
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        print("new password",user.password)
        db.session.commit()
        flash('Your password has been updated!','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Request Password', form=form)