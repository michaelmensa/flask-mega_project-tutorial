'''
Module: errors: to handle errors. create custom pages for HTTP errors 404
and 500, the two most common ones.
'''

from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    ''' handles 404; not found error '''
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    ''' handles 500; internal error '''
    db.session.rollback()
    return render_template('500.html'), 500
