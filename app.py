from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import shutil

app = Flask(__name__)

# This function fixes the "Read-only file system" error on Vercel
def get_db():
    # 1. Path to the database you uploaded to GitHub
    original_db = os.path.join(os.path.dirname(__file__), 'database.db')
    
    # 2. Path to the ONLY folder Vercel allows us to write to
    target_db = '/tmp/database.db'

    # 3. Copy the database to the writable folder if it's not already there
    if not os.path.exists(target_db):
        # This handles the case where the file might not exist yet
        if os.path.exists(original_db):
            shutil.copy2(original_db, target_db)
        else:
            # If no DB exists at all, create it and the table
            conn = sqlite3.connect(target_db)
            conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT)')
            conn.close()
    
    conn = sqlite3.connect(target_db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    # Note: index.html MUST be inside a folder named 'templates'
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
    app.run(debug=True)
