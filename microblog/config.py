'''
Module - config: Configuration class for this application.
'''

import os


class Config(object):
    '''
    config class for configuration. takes the object parameter
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
