'''
Module - models: this module defines the structure of the database
'''

from datetime import datetime
from app import app, db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt


@login.user_loader
def load_user(id):
    ''' function that is called to load a user. args=id '''
    return User.query.get(int(id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )


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
    '''
    Association table for followers and following
    '''
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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

    def follow(self, user):
        ''' function to follow a user '''
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        ''' function to unfollow a user '''
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        ''' function to check following '''
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        ''' to view posts by followed by users '''
        '''return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())
        '''
        ''' followed post query with user's own posts '''
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        ''' reset password token '''
        return jwt.encode(
            {'rest_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        ''' verifies password token '''
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


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
