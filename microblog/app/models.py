'''
Module - models: this module defines the structure of the database
'''

from datetime import datetime
from app import db


class User(db.Model):
    '''
    User model that takes:
    id, username, email and password_hash
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        '''
        returns '<User {}>'.format(self.username)
        '''
        return '<User {}>'.format(self.username)


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
