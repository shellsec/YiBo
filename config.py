#!/usr/bin/env python3
# encoding: utf-8

class Config():
    YiBo_Path = '/root/Desktop/'	# YiBo文件夹存放目录（只修改此目录即可）
    DATABASE = YiBo_Path + 'YiBo/entries.db'	# sqlite数据库文件
    HTML_FOLDER = YiBo_Path + 'YiBo/templates/article/'		# 生成的文章存放路径
    ALLOWED_EXTENSIONS = {'md'}		# 允许上传的文件类型
    DEBUG = True
    SECRET_KEY = '1111222333'	# session加密key
    USERNAME = 'admin'		# 博客管理用户帐号
    PASSWORD = 'admin'		# 博客管理用户密码
conf = {
    'default' : Config
}
