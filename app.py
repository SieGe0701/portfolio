
from flask import Flask, render_template, request, redirect, url_for, session
import uuid

from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import os




from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = 'change_this_secret_key'  # Needed for session


# Multi-admin login for blog admin (for delete button visibility)

# Supabase client setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY must be set in .env")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_admin(username, password):
    password_hash = generate_password_hash(password)
    # Insert admin if not exists
    existing = supabase.table("admins").select("username").eq("username", username).execute()
    if not existing.data:
        supabase.table("admins").insert({"username": username, "password": password_hash}).execute()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('is_admin'):
        return redirect(url_for('blog'))
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        res = supabase.table("admins").select("password").eq("username", username).single().execute()
        row = res.data if res.data else None
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
    res = supabase.table("blog_posts").select("id, title, content, date").order("date", desc=True).execute()
    rows = res.data if res.data else []
    return [
        {'id': row['id'], 'title': row['title'], 'content': row['content'], 'date': row['date']}
        for row in rows
    ]

def get_post(post_id):
    res = supabase.table("blog_posts").select("id, title, content, date").eq("id", post_id).single().execute()
    row = res.data if res.data else None
    if row:
        return {'id': row['id'], 'title': row['title'], 'content': row['content'], 'date': row['date']}
    return None

def add_post(title, content, date):
    post_id = str(uuid.uuid4())
    supabase.table("blog_posts").insert({"id": post_id, "title": title, "content": content, "date": date}).execute()
    return post_id

def delete_post(post_id):
    supabase.table("blog_posts").delete().eq("id", post_id).execute()


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
                existing = supabase.table("admins").select("username").eq("username", new_username).execute()
                if existing.data:
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
