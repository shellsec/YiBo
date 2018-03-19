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

def db_connect():
    return sqlite3.connect(app.config.get('DATABASE'))

@app.before_request
def before_request():
    g.db = db_connect()

@app.teardown_request
def teardown_request(Exception):
    g.db.close()


@app.route('/add',methods = ['POST'])
def add():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    file = request.files['file']
    if file and allowed_file(file.filename):
        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
                'markdown.extensions.toc']
        mdstr = file.read()
        htmlmd = markdown.markdown(mdstr.decode('utf-8'), extensions=exts)
        htmlstr = render_template('mob.html', htmlmd = htmlmd)
        htmlfilepath = app.config.get('HTML_FOLDER') + str(random.randint(10000, 99999)) + '.html'
        with open(htmlfilepath, 'w') as f:
            f.write(htmlstr)
        title = file.filename.rsplit('.', 1)[0]
        text = htmlfilepath[-10:-5]
        g.db.execute('insert into entries (title, text) VALUES (?, ?)', [title, text])
        g.db.commit()
        flash('Successfully posted')
        return redirect(url_for('index'))
    else:
        error = "Please upload md file."
        return render_template('index.html', error=error)


@app.route('/')
def index():
    if request.args.get('file',''):
        fileurl = app.config.get('HTML_FOLDER')+request.args.get('file','')+'.html'
        if os.path.exists(fileurl):
            return render_template('./article/'+request.args.get('file','')+'.html')
        else:
            error = "The article does not exist."
            return render_template('index.html', error=error)
    cur = g.db.execute('select title, text from entries ORDER BY id DESC ')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('index.html', entries = entries)

@app.route('/login',methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('Logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
