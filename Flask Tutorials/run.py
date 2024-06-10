from flaskblog import app
from flaskblog import db
from flaskblog.models import User, Post


if __name__ == '__main__':
    # with app.app_context():
    #     # db.drop_all()  # Drop all existing tables
    #     # db.create_all()  # Recreate tables

    app.run(debug=True)
