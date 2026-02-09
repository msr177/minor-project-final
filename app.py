from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
app = Flask(__name__)
app = Flask(__name__)
app.debug = True  
app = app         
def get_db():
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    return render_template('index.html', users=users)
@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    db = get_db()
    db.execute('INSERT INTO users (username, email) VALUES (?, ?)', (username, email))
    db.commit()
    db.close()
    return redirect(url_for('index'))
@app.route('/delete/<int:id>')
def delete_user(id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run()