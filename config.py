#!/usr/bin/env python3
# encoding: utf-8

class Config():
    YiBo_Path = '/root/'
    DATABASE = YiBo_Path + 'YiBo/entries.db'
    HTML_FOLDER = YiBo_Path + 'YiBo/templates/article/'
    ALLOWED_EXTENSIONS = {'md'}
    DEBUG = True
    SECRET_KEY = '1111222333'
    USERNAME = 'admin'
    PASSWORD = 'admin'
conf = {
    'default' : Config
}
