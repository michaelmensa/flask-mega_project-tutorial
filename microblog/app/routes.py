'''
Module - routes: the routes are the different URLs that the application implements. 
'''

from app import app


@app.route('/')
@app.route('/index')
def index():
    ''' returns Hello, World! '''
    return "Hello, Worlk!"