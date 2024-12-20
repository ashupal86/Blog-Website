from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from methods import User, POSTS, Admin, close_db
import json
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
app.teardown_appcontext(close_db)
app.secret_key = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

user = User()
posts = POSTS()

# Initialize Admin class within app context
admin = Admin(app)

limiter = Limiter(
    get_remote_address,  
    app=app,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri="memcached://localhost:11211",
    storage_options={}
)


# Example decorator to check if user is logged in
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'credentials' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


default=limiter.shared_limit("10 per minute",scope="default")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
@default
def about():
    return render_template('about.html')

@app.route('/search',methods=['GET'])
def search():
    query=request.args.get('q')
    if query:
        
        response=posts.search_post(query)
        
                

        return response
    else:
        return posts.get_posts(0)
    
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    try:
    
        if 'credentials' in session:
            return redirect(url_for('dashboard'))
        else:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                response = user.login(username, password)
                result = json.loads(response)
                if result['status'] == 200:
                    session['credentials'] = username
                    flash('You were successfully logged in', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash(result['msg'], 'danger')
        return render_template('login_registration.html')
    except Exception as e:
        flash('Something went Wrong','danger')
        return redirect('/')

@app.route('/register', methods=['POST'])
@limiter.limit("2 per minute")
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    age = request.form['age']
    phone_number = request.form['phone_number']
    response = user.register(username, password, email, age, phone_number)
    result = json.loads(response)
    if result['status'] == 200:
        flash('You were successfully registered', 'success')
        return redirect(url_for('login'))
    else:
        flash(result['msg'], 'danger')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['credentials'] 
    
    return render_template('profile.html', username=username)

@app.route('/get_user_post', methods=['POST'])
@login_required
def user_post():
    username = session['credentials']
    get_posts = posts.get_user_posts(username)
    data = json.loads(get_posts)
    # print(data)
    return jsonify(data)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))



@app.route('/create_post', methods=['GET', 'POST'])
@login_required
@limiter.limit("1 per minute")
def create_post():
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        post_author = session['credentials']
        tags = request.form['tags']
        response = posts.create_post(post_title, post_content, post_author, tags)
        result = json.loads(response)
        if result['status'] == 200:
            flash(result['msg'], 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['msg'], 'danger')
    return render_template('create_post.html')

@app.route('/edit_post/<postid>', methods=['GET', 'POST'])
@login_required
def edit_post(postid):
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        post_author = session['credentials']
        tags = request.form['tags']
        response = posts.edit_post(postid, post_title, post_content, post_author, tags)
        result = json.loads(response)
        if result['status'] == 200:
            flash(result['msg'], 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result['msg'], 'danger')
    return render_template('create_post.html',title='Edit Post',post=json.loads(posts.get_post_by_id(postid)))

@app.route('/get_posts/<page>')
@app.route('/get_posts',defaults={'page':'1'})
def get_posts(page):
    post=10
    offset=(int(page)-1)*post

    response = posts.get_posts(offset)
    data = json.loads(response)
    if data['status'] == 200:
        return jsonify(data)
    else:
        return jsonify({"error": data['msg']})
    

    
# add a route that allow us to share post using post id
@app.route('/post/<postid>')
@limiter.limit("5 per minute")
def share(postid):
    response=posts.get_post_by_id(postid)
    
    data=json.loads(response)
    # print(data.get('status'))
    return render_template('post.html',post=data)

@app.route('/delete_post',methods=['POST'])
@login_required
def delete_post():
    if request.method=="POST":
        data=request.get_json()
        post_id=data.get('postid')
        author=data.get('author')
        if session['credentials']==author:
            response=posts.delete_post(post_id)
            result=json.loads(response)
            # print(result['msg'])
            if result['status']==200:
                flash(result['msg'],'success')
                return result
            else:
                flash(result['msg'],'danger')
                return result
        flash('Login First','danger')
    return redirect(url_for('dashboard'))


@app.route('/load_deleted',methods=['GET'])
@login_required
def load_deleted():
    username=session['credentials']
    response=posts.get_deleted_posts(username)
    data=json.loads(response)
    return jsonify(data)

@app.route('/restore_post',methods=['POST'])
@login_required
def restore_post():
    if request.method=="POST":
        data=request.get_json()
        post_id=data.get('postid')
        author=data.get('author')
        if session['credentials']==author:
            response=posts.restore_post(post_id)
            result=json.loads(response)
            # print(result['msg'])
            if result['status']==200:
                flash(result['msg'],'success')
                return result
            else:
                flash(result['msg'],'danger')
                return result
        flash('Login First','danger')
    return redirect(url_for('dashboard'))

    


    

# Admin routes
@app.route('/admin_login', methods=['GET', 'POST'])
@limiter.limit("2 per minute")
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if admin.authenticate(username, password):
            session['admin'] = username
            flash('Admin login successful', 'success')
            return redirect(url_for('admin_'))
        else:
            flash('Invalid admin credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin')
def admin_():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    
    get_users = admin.get_registered_users()
    pending_users = admin.get_pending_users()
    


    # Convert rows to dictionaries
    get_users_list = [dict(row) for row in get_users]
    pending_users_list = [dict(row) for row in pending_users]
    
    return render_template('admin.html', users=get_users_list, pending_users=pending_users_list)


@app.route('/load_deleted_posts', methods=['GET'])
def load_deleted_posts():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    deleted_posts = posts.get_all_deleted_posts()
    return jsonify(json.loads(deleted_posts))

@app.route('/approve_user', methods=['POST'])
def approve_user():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        admin.approve_user(user_id)
        return jsonify({"status": 200})
    return jsonify({"status": "error", "msg": "Invalid user ID"}), 400

@app.route('/deny_user', methods=['POST'])
def deny_user():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        try:
            admin.deny_user(user_id)
            return jsonify({"status": 200})
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500
    return jsonify({"status": "error", "msg": "Invalid user ID"}), 400

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        try:
            admin.delete_user(user_id)
            return jsonify({"status": 200})
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500
    return jsonify({"status": "error", "msg": "Invalid user ID"}), 400

@app.route('/add_admin', methods=['POST'])
def add_admin():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(username, password)
    if username and password:
        try:
            admin.add_admin(username, password)
            return jsonify({"status": "success", "msg": "Admin added successfully"})
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500
    return jsonify({"status": "error", "msg": "Username and password required"}), 400

@app.route('/reset_password', methods=['POST'])
def reset_password():
    if 'admin' not in session:
        flash('Admin access required', 'danger')
        return redirect(url_for('admin_login'))
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    if username and new_password:
        try:
            admin.reset_password(username, new_password)
            return jsonify({"status": "success", "msg": "Password reset successfully"})
        except Exception as e:
            return jsonify({"status": "error", "msg": str(e)}), 500
    return jsonify({"status": "error", "msg": "Username and new password required"}), 400

@app.route('/logout_admin', methods=['POST'])
def logout_admin():
    session.clear()
    flash('Admin has been logged out', 'info')
    return redirect(url_for('admin_login'))


@app.errorhandler(429)  # Too Many Requests
def ratelimit_error(e):
    return jsonify(error="Rate limit exceeded. Try again later."), 429



