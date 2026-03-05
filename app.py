import os
from flask import Flask, render_template, request, session, redirect, render_template_string, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from fuzzywuzzy import fuzz
import json


app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'))
app.secret_key = 'super-secret-key'

# Load config parameters
with app.open_instance_resource('config.json') as config_file:
    params = json.load(config_file)["params"]

# Ensure instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

# Database Connection
if params['local_server']:
    db_path = os.path.join(app.instance_path, 'mydatabase.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']

db = SQLAlchemy(app)


# Database Models
class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.Text, nullable=True)
    author = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False, default="General")
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    liked_by = db.relationship('UserPostLike', backref='post', lazy=True)
    


class UserPostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.sno'))
    is_like = db.Column(db.Boolean, nullable=False)  # True = like, False = dislike

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.sno'), nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')


class Pending_Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text)
    author = db.Column(db.Text, nullable=False)
    slug = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, default="General")
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    phone_num = db.Column(db.Text, nullable=False)
    mes = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, nullable=False, unique=True)
    pass_word = db.Column(db.Text, nullable=False)
    

# Create all tables
with app.app_context():
    db.create_all()

# Index Page Route
@app.route('/')
def home():
    category_filter = request.args.get('category', 'All')
    sort_by = request.args.get('sort_by', '')  # Get the sort option from the query string
    page = request.args.get('page', 1, type=int)  # Get current page number (default to 1)
    per_page = 9  # Number of posts per page




    # Start the base query
    if category_filter == 'All':
        query = Post.query
    else:
        query = Post.query.filter_by(category=category_filter)

    # Apply sorting based on user selection
    if sort_by == 'latest':
        query = query.order_by(Post.date.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Post.date.asc())
    elif sort_by == 'likes':
        query = query.order_by(Post.likes.desc())
    else:
        query = query.order_by(Post.date.desc())  # Default sorting by latest

    # Fetch the posts with limit
    # _posts = query.limit(params['no_of_posts']).all()
    # Apply pagination
    posts = query.paginate(page=page, per_page=per_page, error_out=False)



    return render_template('index.html', posts=posts, params=params, selected_category=category_filter)

# About Page Route
@app.route('/about')
def about():
    return render_template('about.html', params=params)

# # Contact Page Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'user' in session and session['user'] == params['admin_username']:  
        # If admin, show messages instead of form
        messages = Contact.query.order_by(Contact.date.desc()).all()  
        return render_template('admin_messages.html', messages=messages, params=params)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        mes = request.form.get('message')

        entry = Contact(name=name, phone_num=phone, mes=mes, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html', params=params)  # Normal users see the contact form

# Route to display a post based on its slug
@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    if not post:
        return "Post not found", 404
    
    comments = Comment.query.filter_by(post_id=post.sno).order_by(Comment.date.desc()).all()
    # Fetch likes/dislikes from the Post table
    likes = post.likes
    dislikes = post.dislikes
    return render_template('post.html', post=post, params=params, likes=likes, dislikes=dislikes,comments=comments)

# Dashboard Page Route
@app.route("/dashboard")
def dashboard():
    # Check if the user is logged in and is the admin
    if 'user' in session and session['user'] == params['admin_username']:
        action = request.args.get('action')  # Retrieve action parameter from URL
        sno = request.args.get('sno', type=int)  # Retrieve post serial number (sno) and convert to int
        username = request.args.get('username')  # Retrieve username from URL parameters

        # Render the pending posts page (Triggered from dashboard.html)
        if action == "render_pending_post":  
            _pending_posts = Pending_Post.query.all()
            return render_template('pending_posts.html', params=params, posts=_pending_posts)
        
        # Approve a pending post and move it to the main posts table (Triggered from pending_posts.html)
        elif action == "approve_post" and sno is not None:  
            post = Pending_Post.query.filter_by(sno=sno).first()  # Find the post in Pending_Post table
            if post:
                approved_post = Post(
                    title=post.title, subtitle=post.subtitle, author=post.author,
                    slug=post.slug, content=post.content, category=post.category, date=post.date
                )
                db.session.add(approved_post)
                db.session.delete(post)  # Remove post from the Pending_Post table
                db.session.commit()
                return redirect('/dashboard')  # Redirect back to the dashboard
        
        # Render the user management page (Triggered from dashboard.html)
        elif action == "render_manage_users":  
            users = User.query.all()
            return render_template('users.html', params=params, users=users)
        
        # Remove a user from the database (Triggered from users.html)
        elif action == "remove_user":  
            user_ = User.query.filter_by(user_name=username).first()
            if user_:
                db.session.delete(user_)
                db.session.commit()
                return redirect('/dashboard')
        
        # Default: Render the dashboard with all approved posts
        # (Accessed by default or after an action from various pages)
        _posts = Post.query.all()
        response = make_response(render_template('dashboard.html', params=params, posts=_posts))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    
    else:
        return redirect('/')  # Redirect to the home page if the user is not authorized

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Edit Post Route
@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session:
        user = User.query.filter_by(user_name=session['user']).first()  # Retrieve logged-in user details

        if request.method == 'POST':
            _title = request.form.get('title')
            _subtitle = request.form.get('subtitle')
            _author = "Admin" if session['user'] == params['admin_username'] else user.user_name
            _slug = request.form.get('slug')
            _content = request.form.get('content')
            _date = datetime.now(timezone.utc)
            _category = request.form.get('category')  # Retrieve selected category
            
            # Admin or user adding a new post (Triggered from edit.html with sno='0')
            if sno == '0':
                if session['user'] == params['admin_username']:  # Admin adding a new post
                    post = Post(
                        title=_title, subtitle=_subtitle, author=_author,
                        slug=_slug, content=_content,category=_category, date=_date
                    )
                    db.session.add(post)
                    db.session.commit()
                    return redirect('/dashboard')  # Redirect to dashboard after posting
                
                else:  # Regular user submitting a new post (Goes to pending review)
                    post = Pending_Post(
                        title=_title, subtitle=_subtitle, author=_author,
                        slug=_slug, content=_content,category=_category, date=_date
                    )
                    db.session.add(post)
                    db.session.commit()
                    # session.pop('user')  # Log the user out after submission
                    return redirect('/')  # Redirect to home page

            # Editing an existing post (Triggered from edit.html with valid sno)
            else:
                post = Post.query.filter_by(sno=sno).first()
                if post.author == params['admin_username']:  # Admin editing their own post
                    post.title = _title
                    post.subtitle = _subtitle
                    post.slug = _slug
                    post.content = _content
                    post.category=_category
                    post.date = _date
                    db.session.add(post)
                    db.session.commit()
                    return redirect('/dashboard')  # Redirect back to dashboard
                
                else:  # Admin cannot edit posts created by regular users
                    return render_template_string("""
                        <h1>Error</h1>
                        <p>Admin does not have permission to edit other posts.</p>
                    """)

        # Render the edit post page (Triggered from dashboard.html or edit.html)
        _post = Post.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=_post, sno=sno)


# Route to delete a post (either pending or published)
@app.route("/delete")
def delete():
    # Ensure only the admin can delete
    if 'user' in session and session['user']==params['admin_username']:
        action = request.args.get('action')  # Get action from URL
        sno = request.args.get('sno', type=int)  # Get sno and convert to int

        if action == "delete_pending_post": # Deleting a pending post (Triggered from pending_posts.html)
            _post = Pending_Post.query.filter_by(sno=sno).first()  # Fetch the specific pending post
            db.session.delete(_post)
            db.session.commit()
        elif action == "delete_post": # Deleting a published post (Triggered from dashboard.html)
            _post = Post.query.filter_by(sno=sno).first()  # Fetch the specific published post
            if _post:
                # Delete associated comments first
                Comment.query.filter_by(post_id=_post.sno).delete()
           
            db.session.delete(_post)
            db.session.commit()
        
        return redirect('/dashboard')

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Route for user and admin login
@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')  # Capture ?next= from URL

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Admin login check
        if username == params['admin_username'] and password == params['admin_password']:
            session['user'] = params['admin_username']
            return redirect(next_page or '/')  # Admin redirected to dashboard

        # Check if user exists in the database
        user = User.query.filter_by(user_name=username, pass_word=password).first()
        if user:
            session['user'] = user.user_name
            return redirect(next_page or '/')  # ✅ Normal user redirected to Home if no next
        else:
            return render_template('login.html', params=params, error="Invalid credentials")

    # Render login page with cache disabled
    response = make_response(render_template('login.html', params=params))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

# Route for user registration (Sign-Up)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        _username = request.form.get('username')
        _psw = request.form.get('psw')

        # Check if the username is already taken
        existing_user = User.query.filter_by(user_name=_username).first()
        if existing_user:
            return render_template('signup.html', error="Username already taken")
        
        # Create a new user and add to database
        user = User(user_name=_username, pass_word=_psw)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/login')  # Redirect to login page after successful sign-up
    
    return render_template('signup.html')  # Render sign-up page for GET request

@app.route('/like_dislike/<int:post_id>/<string:action>', methods=['POST'])
def like_dislike(post_id, action):
    if 'user' not in session:
        # Redirect to login and pass the action as 'next'
        return redirect(f'/login?next=/like_dislike/{post_id}/{action}')

    user = User.query.filter_by(user_name=session['user']).first()
    post = Post.query.get(post_id)

    if not user or not post:
        return redirect('/')

    # Like/Dislike logic
    existing = UserPostLike.query.filter_by(user_id=user.id, post_id=post_id).first()

    if existing:
        if (action == 'like' and existing.is_like) or (action == 'dislike' and not existing.is_like):
            # Undo the action
            if existing.is_like:
                post.likes = max(post.likes - 1, 0)
            else:
                post.dislikes = max(post.dislikes - 1, 0)
            db.session.delete(existing)
        else:
            # Switch action
            if action == 'like':
                post.likes += 1
                post.dislikes = max(post.dislikes - 1, 0)
                existing.is_like = True
            else:
                post.dislikes += 1
                post.likes = max(post.likes - 1, 0)
                existing.is_like = False
            db.session.commit()
    else:
        # New like/dislike
        new_like = UserPostLike(user_id=user.id, post_id=post_id, is_like=True if action == 'like' else False)
        db.session.add(new_like)
        if action == 'like':
            post.likes += 1
        else:
            post.dislikes += 1

    db.session.commit()
    return redirect(f"/post/{post.slug}")

@app.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if 'user' not in session:
        # Redirect to login with next pointing back to this comment action
        return redirect(f"/login?next=/comment/{post_id}")

    user = User.query.filter_by(user_name=session['user']).first()
    post = Post.query.get(post_id)

    if not user or not post:
        # Redirect safely to home if invalid post or user
        return redirect('/')

    comment_text = request.form.get('comment')
    if not comment_text or not comment_text.strip():
        # Optionally, flash a message that the comment was empty (for better UX)
        return redirect(f"/post/{post.slug}")

    # Save the comment
    new_comment = Comment(content=comment_text.strip(), user_id=user.id, post_id=post.sno)
    db.session.add(new_comment)
    db.session.commit()

    # Redirect back to the post after adding the comment
    return redirect(f"/post/{post.slug}")


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        if not query:
            return render_template('search.html', posts=[], params=params, query=query)

        all_posts = Post.query.all()
        matched_posts = []

        for post in all_posts:
            # Perform fuzzy match on title and content
            title_score = fuzz.partial_ratio(query.lower(), post.title.lower())
            content_score = fuzz.partial_ratio(query.lower(), post.content.lower())
            category_score = fuzz.partial_ratio(query.lower(), post.category.lower())

            # You can set the threshold (adjust based on how vague you want matching to be)
            if title_score > 60 or content_score > 60 or category_score > 60:
                matched_posts.append(post)

        return render_template('search.html', posts=matched_posts, params=params, query=query)

    return render_template('search.html', posts=[], params=params)


# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(debug=True)
