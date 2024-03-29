import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash , redirect, send_file, send_from_directory, request, abort
from nosy import app, db, bcrypt, mail
from nosy.models import User,Post
from nosy.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, UpdatePostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import time

@app.route("/home")
@login_required
def home():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html',posts=posts)

@app.route("/")
@app.route("/about")
def about():
	return render_template('about.html',title ='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user,remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account",methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			if current_user.image_file != 'default.jpg':
				os.remove(os.path.join(app.config['UPLOADED_PROFILE_PIC'], current_user.image_file))
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your particulars have been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/user/<string:username>")
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_posts.html',posts=posts, user=user)



def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn

def upload_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
	output_size = (570,500)
	i = Image.open(form_picture)
	i = i.resize(output_size, Image.ANTIALIAS)
	i.save(picture_path, quality=500)
	return picture_fn

@app.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = upload_picture(form.picture.data)
		else:
			picture_file = 'NULL'
		post = Post(title=form.title.data,content=form.content.data,image_file=picture_file,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success') 
		return redirect(url_for('home'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/download")
def download():
	return render_template('download.html')

@app.route("/video")
def video():
	return render_template('video.html')

@app.route("/webguide")
def webguide():
	return render_template('webguide.html')

@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Nosy Password Reset Request', sender='boyzbackend@gmail.com', recipients=[user.email])
	msg.body= f'''To reset your password, visit the following link:

{url_for('reset_token',token=token, _external=True)}

Ignore this email if you did not submit this request.
'''
	mail.send(msg)


@app.route("/reset_password",methods=['GET', 'POST'])
def reset_request():
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		form = RequestResetForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			send_reset_email(user)
			flash('An email has been sent with instructions to reset your password.', 'info')
			return redirect(url_for('login'))
		return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>",methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
			return redirect(url_for('home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('Invalid or expired token.','warning')
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated!', 'success')
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)



@app.route("/post/<int:post_id>/update",methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = UpdatePostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		if form.delete_image and post.image_file != 'NULL':
			os.remove(os.path.join(app.config['UPLOADED_POSTS_DEST'], post.image_file))
			post.image_file = 'NULL'
		if form.picture.data:
			post.image_file = upload_picture(form.picture.data)
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('update_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	if post.image_file != 'NULL':
		os.remove(os.path.join(app.config['UPLOADED_POSTS_DEST'], post.image_file))
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted.', 'success')
	return redirect(url_for('home'))

@app.route("/demo")
def demo():
	return render_template('demo.html',title ='Demo')


@app.route("/demo/discover_all")
def discover_all():
	return render_template('discover_all.html',title ='Demo')

@app.route("/demo/scan_iot")
def scan_iot():
	return render_template('scan_iot.html',title ='Demo')

@app.route("/demo/display_traffic")
def display_traffic():
	return render_template('display_traffic.html',title ='Demo')

@app.route("/demo/discover_all/discovered_all")
def discovered_all():
	time.sleep(5)
	return render_template('discovered_all.html',title ='Demo')

@app.route("/demo/scanned_iot")
def scanned_iot():
	time.sleep(5)
	return render_template('scanned_iot.html',title ='Demo')

#so change the link to downloads/###.py to download that file
@app.route("/downloads/<image_name>")
@login_required
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)



