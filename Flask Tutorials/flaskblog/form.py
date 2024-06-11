from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from flaskblog.models import User, Post
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm_Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if(user):
            raise ValidationError('Email Taken! Choose another email!')


class LoginForm(FlaskForm):
    email=StringField('Enail',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Always Remember Me')
    submit=SubmitField('Login')

class AccountUpdateForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(), Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(), Email()])
    picture=FileField('Upload Picture',validators=[FileAllowed(['jpg','png'])])
    update=SubmitField('Update')

    def validate_username(self, username):
        if(username.data != current_user.username):
            user=User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError('That Username is already taken!')
        
    def validate_email(self, email):
        if(email.data != current_user.email):
            user=User.query.filter_by(email=email.data).first()
            if(user):
                raise ValidationError('That Email is Already taken!')
            
class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(),Length(min=4,max=30)])
    content=TextAreaField('Content',validators=[DataRequired()])
    submit=SubmitField('Upload')
