'''
Module - microblog: Main aplication module
'''


from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    ''' function that makes shell_context '''
    return {'db': db, 'User': User, 'Post': Post}
