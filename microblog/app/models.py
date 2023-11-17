'''
Module - models: this module defines the structure of the database
'''

from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


@login.user_loader
def load_user(id):
    ''' function that is called to load a user. args=id '''
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    '''
    User model that takes:
    id, username, email and password_hash
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        '''
        returns '<User {}>'.format(self.username)
        '''
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        ''' function that sets password args=password '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        ''' function that checks password args=password '''
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        ''' function that provides User avatar URLs '''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicons&s={}'.format(
            digest, size)



class Post(db.Model):
    '''
    Post model that contains the blog post the user publishes
    '''
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        '''
        returns '<Post {}>'.format(self.body)
        '''
        return '<Post {}>'.format(self.body)
