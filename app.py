from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'a-very-secret-key'
DB_PATH = 'users.db'

# --- DB Setup ---
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        # Create users table if it doesn't exist and add 'role' column if missing
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'  -- Added role column with a default value
            )
        ''')

        # Check if the 'role' column exists; if not, add it
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(users);')
        columns = [column[1] for column in cursor.fetchall()]  # Use column[1] for column name
        
        if 'role' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN role TEXT DEFAULT "user";')
            conn.commit()
            print("Role column added to the users table.")

init_db()

# --- Routes ---
@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        # Fetch the user's role from the database
        with sqlite3.connect(DB_PATH) as conn:
            user = conn.execute('SELECT id, username, password, role FROM users WHERE username = ?', (username,)).fetchone()
            if user:
                role = user[3]  
            else:
                flash("User not found!", 'danger')
                return redirect(url_for('login'))
        # Get the list of all users
        with sqlite3.connect(DB_PATH) as conn:
            users = conn.execute('SELECT id, username FROM users').fetchall()

        return render_template('home.html', username=username, role=role, users=users)
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect(DB_PATH) as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'username' not in session:
        flash('You must be logged in to edit users.', 'warning')
        return redirect(url_for('login'))

    # Fetch the user's details from the database
    with sqlite3.connect(DB_PATH) as conn:
        user = conn.execute('SELECT id, username, role FROM users WHERE id = ?', (user_id,)).fetchone()

    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('home'))

    # Handle form submission (POST request)
    if request.method == 'POST':
        new_username = request.form['username']
        new_role = request.form['role']

        # Check if the new username already exists
        with sqlite3.connect(DB_PATH) as conn:
            existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (new_username,)).fetchone()
            if existing_user and existing_user[0] != user_id:
                flash('Username already taken, please choose another one.', 'danger')
                return redirect(url_for('edit_user', user_id=user_id))

        # Update the user's details in the database
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('UPDATE users SET username = ?, role = ? WHERE id = ?', (new_username, new_role, user_id))
            flash('User updated successfully!', 'success')

        return redirect(url_for('home'))

    # Render the edit user form for GET request
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    if 'username' not in session:
        flash('You must be logged in to delete users.', 'warning')
        return redirect(url_for('login'))

    # Connect to the database and delete the user
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        flash(f'User with ID {user_id} deleted successfully.', 'success')

    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form.get('role', 'user')  

        with sqlite3.connect(DB_PATH) as conn:
            try:
                conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
                flash('User registered successfully.', 'success')
            except sqlite3.IntegrityError:
                flash('Username already exists.', 'danger')
                return redirect(request.referrer or url_for('register'))

        # Redirect back depending on login state
        if 'username' in session:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
