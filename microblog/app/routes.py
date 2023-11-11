'''
Module - routes: the routes are the different URLs that the application implements. 
'''

from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    ''' returns Hello, World! '''
    user = {'username': 'Michael'}
    posts = [
            {
                'author': {'username': 'Miguel'},
                'body': 'Beautiful day in Portland'
                },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
                }
            ]
    return render_template('index.html', title='Home', user=user, posts=posts)
