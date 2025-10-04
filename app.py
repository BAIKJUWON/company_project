from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import Markup
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 전역 글꼴 설정 (나눔스퀘어)
@app.context_processor
def inject_font():
    font_tag = Markup("""
    <link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@1.0/nanumsquare.css" rel="stylesheet">
    <style>
        body {
            font-family: 'NanumSquare', sans-serif;
        }
    </style>
    """)
    return dict(global_font=font_tag)

# 모델 정의
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), default=datetime.now().strftime("%Y-%m-%d"))
    approved = db.Column(db.Boolean, default=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    name = db.Column(db.String(30))
    role = db.Column(db.String(10), default='pending')  # admin / manager / user / pending

@app.before_request
def init_db():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True

@app.route('/')
def index():
    photos = Post.query.filter_by(category='photo', approved=True).all()
    notices = Post.query.filter_by(category='notice', approved=True).all()
    return render_template('index.html', photos=photos, notices=notices)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uid = request.form['username']
        pw = request.form['password']
        user = User.query.filter_by(username=uid, password=pw).first()
        if user:
            if user.role != 'pending':
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                return redirect('/')
            else:
                return '관리자 승인 후 사용 가능합니다.'
        return '아이디 또는 비밀번호 오류'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/new_p', methods=['GET', 'POST'])
def new_p():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        role = 'admin' if User.query.count() == 0 else 'pending'
        new_user = User(username=username, password=password, name=name, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('new_p.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') == 'pending':
        return '관리자 승인 후 게시물 작성이 가능합니다.'

    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        image = request.files.get('image', None)

        if image and image.filename != '':
            filename = f"{datetime.now().timestamp()}_{image.filename}"
            folder = os.path.join(app.config['UPLOAD_FOLDER'], category)
            os.makedirs(folder, exist_ok=True)
            image_path = f"{category}/{filename}"
            image.save(os.path.join(folder, filename))
        else:
            image_path = 'basic.jpg'

        approved = session.get('role') in ['admin', 'manager']

        new_post = Post(
            title=title,
            category=category,
            image=image_path,
            content=content,
            approved=approved
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

    return render_template('upload.html')

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/news')
def news():
    posts = Post.query.filter_by(category='news', approved=True).all()
    return render_template('news.html', posts=posts, title='보도자료')

@app.route('/notice')
def notice():
    posts = Post.query.filter_by(category='notice', approved=True).all()
    return render_template('notice.html', posts=posts, title='공지사항')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/imagepage')
def imagepage():
    posts = Post.query.filter_by(category='photo', approved=True).all()
    return render_template('imagepage.html', posts=posts, title='활동사진')

@app.route('/admin')
def admin():
    if session.get('role') not in ['admin', 'manager']:
        return redirect('/')
    posts = Post.query.all()
    users = User.query.all()
    return render_template('admin.html', posts=posts, users=users)

@app.route('/set_role/<int:user_id>/<role>')
def set_role(user_id, role):
    if session.get('role') != 'admin':
        return redirect('/')
    user = User.query.get(user_id)
    if not user:
        return redirect('/admin')
    user.role = role
    db.session.commit()
    return redirect('/admin')

@app.route('/approve_post/<int:post_id>')
def approve_post(post_id):
    if session.get('role') not in ['admin', 'manager']:
        return redirect('/')
    post = Post.query.get_or_404(post_id)
    post.approved = True
    db.session.commit()
    return redirect('/admin')

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    if session.get('role') not in ['admin', 'manager']:
        return redirect('/')
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/admin')

# ▶ 회원 삭제 기능 (관리자 전용)
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    if session.get('role') != 'admin':
        return redirect('/')
    if session.get('user_id') == user_id:  # 본인 계정은 삭제 불가
        return redirect('/admin')
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
