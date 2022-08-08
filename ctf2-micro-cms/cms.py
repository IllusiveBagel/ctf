import os
import sqlite3
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, redirect, url_for, abort

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('./database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            admin = request.form['admin']

            if not title:
                flash('Title is required!')
            elif not content:
                flash('Content is required!')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO posts (title, content, admin) VALUES (?, ?, ?)',
                            (title, content, admin))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('create.html')

@app.route('/login', methods=['POST'])
def do_admin_login():

    conn = get_db_connection()
    sql = "SELECT * FROM users WHERE username = '" + request.form['username'] + "'"

    try:
        users = conn.execute(sql)
        for user in users:
            if user['password'] == request.form['password']:
                session['logged_in'] = True
    except sqlite3.Error as er:
        flash(er.args[0])

    conn.close()
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)

app.run(debug=True,host='0.0.0.0', port=4000)