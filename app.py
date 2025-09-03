
from flask import Flask, render_template, request, redirect, url_for, session
import uuid

import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os




from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'change_this_secret_key'  # Needed for session


# Multi-admin login for blog admin (for delete button visibility)
def get_db():
    db_url = os.environ.get("SUPABASE_DB_URL") or os.environ.get("POSTGRES_URL")
    if not db_url:
        raise RuntimeError("SUPABASE_DB_URL or POSTGRES_URL environment variable not set. Please check your .env file.")
    # Remove quotes if present (for compatibility with .env syntax)
    if db_url.startswith('"') and db_url.endswith('"'):
        db_url = db_url[1:-1]
        db_url = os.environ.get("CON_STRING") or os.environ.get("SUPABASE_DB_URL") or os.environ.get("POSTGRES_URL")
        if not db_url:
            raise RuntimeError("CON_STRING, SUPABASE_DB_URL, or POSTGRES_URL environment variable not set. Please check your .env file.")
        # Remove quotes if present (for compatibility with .env syntax)
        if db_url.startswith('"') and db_url.endswith('"'):
            db_url = db_url[1:-1]
        # Remove 'supa' query param if present
        import re
        if 'supa=' in db_url:
            # Remove supa=... from query string
            db_url = re.sub(r'([&?])supa=[^&]*&?', lambda m: m.group(1) if m.group(0).endswith('&') else '', db_url)
            # Clean up any trailing ? or &
            db_url = re.sub(r'[?&]$', '', db_url)
            db_url = db_url.replace('?&', '?')
        return psycopg2.connect(db_url, cursor_factory=RealDictCursor)

def add_admin(username, password):
    password_hash = generate_password_hash(password)
    with get_db() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO admins (username, password) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING', (username, password_hash))
        conn.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('blog'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with get_db() as conn:
            with conn.cursor() as c:
                c.execute('SELECT password FROM admins WHERE username = %s', (username,))
                row = c.fetchone()
        if row and check_password_hash(row['password'], password):
            session['is_admin'] = True
            session['admin_user'] = username
            return redirect(url_for('blog'))
        else:
            error = 'Invalid credentials.'
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    session.pop('admin_user', None)
    return redirect(url_for('blog'))


# --- Database Setup ---
# Use /tmp for SQLite on Vercel (writable directory in serverless)
if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV'):
    DB_PATH = '/tmp/blog.db'
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), 'blog.db')


# Remove init_db, assume tables are created in Supabase

def get_all_posts():
    with get_db() as conn:
        with conn.cursor() as c:
            c.execute('SELECT id, title, content, date FROM blog_posts ORDER BY date DESC')
            rows = c.fetchall()
            return [
                {'id': row['id'], 'title': row['title'], 'content': row['content'], 'date': row['date']}
                for row in rows
            ]

def get_post(post_id):
    with get_db() as conn:
        with conn.cursor() as c:
            c.execute('SELECT id, title, content, date FROM blog_posts WHERE id = %s', (post_id,))
            row = c.fetchone()
            if row:
                return {'id': row['id'], 'title': row['title'], 'content': row['content'], 'date': row['date']}
            return None

def add_post(title, content, date):
    post_id = str(uuid.uuid4())
    with get_db() as conn:
        with conn.cursor() as c:
            c.execute('INSERT INTO blog_posts (id, title, content, date) VALUES (%s, %s, %s, %s)',
                      (post_id, title, content, date))
        conn.commit()
    return post_id

def delete_post(post_id):
    with get_db() as conn:
        with conn.cursor() as c:
            c.execute('DELETE FROM blog_posts WHERE id = %s', (post_id,))
        conn.commit()


# Blog list and add post
@app.route('/blog', methods=['GET', 'POST'])
def blog():
    from datetime import datetime
    error = None
    success = None
    if request.method == 'POST':
        if session.get('is_admin') and request.form.get('action') == 'add_admin':
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')
            if not new_username or not new_password:
                error = 'Username and password required to add admin.'
            else:
                with get_db() as conn:
                    with conn.cursor() as c:
                        c.execute('SELECT * FROM admins WHERE username = %s', (new_username,))
                        if c.fetchone():
                            error = 'Admin already exists.'
                        else:
                            add_admin(new_username, new_password)
                            success = f'Admin {new_username} added.'
        elif request.form.get('title') and request.form.get('content'):
            title = request.form.get('title')
            content = request.form.get('content')
            add_post(title, content, datetime.now().strftime('%Y-%m-%d %H:%M'))
            return redirect(url_for('blog'))
    posts = get_all_posts()
    previews = [
        {
            'id': post['id'],
            'title': post['title'],
            'date': post['date'],
            'preview': post['content'][:200] + ('...' if len(post['content']) > 200 else '')
        }
        for post in posts
    ]
    return render_template('blog_list.html', posts=previews, error=error, success=success)


# Individual blog post view and delete
@app.route('/blog/<post_id>', methods=['GET', 'POST'])
def blog_post(post_id):
    post = get_post(post_id)
    if not post:
        return render_template('blog_post.html', post=None), 404
    if request.method == 'POST' and request.form.get('delete') == '1':
        delete_post(post_id)
        return redirect(url_for('blog'))
    is_admin = session.get('is_admin', False)
    return render_template('blog_post.html', post=post, is_admin=is_admin)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/Work_Experience')
def skills():
    return render_template('Work_Experience.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')



# No DB init needed for Supabase/Postgres

if __name__ == '__main__':
    app.run()
