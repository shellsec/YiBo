#!/usr/bin/env python3
# encoding: utf-8

# by FoxRoot [www.foxroot.cn]

from flask import Flask, g, render_template, session, request, flash, redirect, url_for
import markdown
import os
from config import *
import sqlite3
import random

app = Flask(__name__)
app.config.from_object(conf['default'])

# 数据库连接


def db_connect():
    return sqlite3.connect(app.config.get('DATABASE'))


@app.before_request
def before_request():
    g.db = db_connect()


@app.teardown_request
def teardown_request(Exception):
    g.db.close()

# 上传文章


@app.route('/add', methods=['POST'])
def add():
    # 检查文件类型
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')
    # 判别session，session不存在则跳转到登录
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    file = request.files['file']
    if file and allowed_file(file.filename):
        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
                'markdown.extensions.toc']
        mdstr = file.read()
        htmlmd = markdown.markdown(mdstr.decode('utf-8'), extensions=exts)
        # 以mob.html为模板，插入md生成的html，并随机保存为html
        htmlstr = render_template('mob.html', htmlmd=htmlmd)
        htmlfilepath = app.config.get(
            'HTML_FOLDER') + str(random.randint(10000, 99999)) + '.html'
        with open(htmlfilepath, 'w') as f:
            f.write(htmlstr)
        title = file.filename.rsplit('.', 1)[0]
        text = htmlfilepath[-10:-5]
        # 文章标题和路径存放到数据库
        g.db.execute(
            'insert into entries (title, text) VALUES (?, ?)', [title, text])
        g.db.commit()
        flash('Successfully posted')
        return redirect(url_for('index'))
    else:
        error = "Please upload md file."
        return render_template('index.html', error=error)

# 主页


@app.route('/')
def index():
    # 有点击链接时，获取file参数，文章存在时跳转到文章
    if request.args.get('file', ''):
        fileurl = app.config.get('HTML_FOLDER') + \
            request.args.get('file', '')+'.html'
        if os.path.exists(fileurl):
            return render_template('./article/'+request.args.get('file', '')+'.html')
        else:
            error = "The article does not exist."
            return render_template('index.html', error=error)
    # 无点击链接时，从数据库输出所有文章标题和地址链接
    cur = g.db.execute('select title, text from entries ORDER BY id DESC ')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries)

# 登录


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('Logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

# 登出


@app.route('/logout')
def logout():
    # 直接注销session来进行登出
    session.pop('logged_in', None)
    flash('Logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
