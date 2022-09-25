from main import *

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)

# PASSWORD ENCRYPTION CONFIG
function = os.environ.get("FUNCTION")
algorithm = os.environ.get("ALGORITHM")
rounds = os.environ.get("SALT_ROUNDS")
salt_length = 64

# ALERT SYMBOLS
success = '<i class="fa-solid fa-circle-check"></i>'
warning = '<i class="fa-solid fa-circle-exclamation"></i>'
danger = '<i class="fa-solid fa-circle-xmark"></i>'


# LOGIN MANAGER
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


login_manager = LoginManager()
login_manager.init_app(app)


# PUBLIC ROUTES
@app.route('/')
def home():
    all_blogs = db.session.query(BlogPost).all()
    return render_template('index.html', blogs=all_blogs)


@app.route('/about')
def about():
    return render_template('about.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = db.session.query(User).filter_by(email=email).first()
            user_pass = f'{function}:{algorithm}:{rounds}${user.password}'
            if user and check_password_hash(user_pass, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash(f"{danger} Password is <strong>incorrect.</strong> Please try again.", 'danger')
                return redirect(url_for("login"))
        except AttributeError:
            flash(f"{warning} That email address is <strong>not registered.</strong> Please register first.", 'warning')
            return redirect(url_for('register'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method=f'{function}:{algorithm}:{rounds}',
            salt_length=salt_length
        ).split('$', 1)[1]

        new_user = User()
        new_user.name = form.name.data
        new_user.email = form.email.data
        new_user.password = hashed_and_salted_password
        new_user.role = "user"

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home"))
        except exc.IntegrityError:
            flash(f"{warning} That email address is <strong>already in use.</strong> Try log in instead!", 'warning')
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/<int:post_id>', methods=["GET", "POST"])
def show_post(post_id):
    comment_form = CommentForm()
    requested_post = db.session.query(BlogPost).get(post_id)
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(f"{warning} You need to <strong>login</strong> or <strong>register</strong> to comment.", 'warning')
            return redirect(url_for("login"))

        new_comment = Comment(
            text=bleach.clean(comment_form.text.data),
            date=date.today().strftime("%B %d, %Y"),
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        flash(f"{success} Your comment has been <strong>added successfully.</strong>", 'success')

    return render_template('post.html', blog=requested_post, form=comment_form)


@app.route("/delete-comment/<int:post_id>/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(post_id, comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    flash(f"{success} Your comment has been <strong>deleted successfully.</strong>", 'success')
    return redirect(url_for('show_post', post_id=post_id))


def sendEmail(data):
    query = f"Subject: {data['subject']}\n\n" \
            f"Name: {data['name']}\n" \
            f"Email: {data['email']}\n" \
            f"Message: {data['message']}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(user=sender_email, password=sender_password)
        server.sendmail(
            from_addr=sender_email,
            to_addrs=f'{data["to"]}',
            msg=query.encode("utf-8")
        )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm() if not current_user.is_authenticated else ContactForm(email=current_user.email)
    if contact_form.validate_on_submit():
        data = {
            "name": contact_form.name.data,
            "email": contact_form.email.data,
            "subject": contact_form.subject.data,
            "message": contact_form.message.data,
            "to": owner_email
        }
        try:
            sendEmail(data)
            flash(f"{success} Thank you for <strong>contacting us.</strong> We will get back to you soon.", 'success')
        except Exception:
            flash(f"{warning} Sorry, <strong>something went wrong.</strong> Please try again later.", 'warning')

    return render_template('contact.html', form=contact_form)


def generateOTP():
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    return otp


# ADMIN-ONLY ROUTES

# HTML SANITIZER
def sanitize_html(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'blockquote', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike', 'strong',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']

    allowed_attrs = {
        'a': ['href', 'target', 'title', 'class', 'style'],
        'img': ['src', 'alt', 'class', 'style'],
        '*': ['class', 'style'],
    }

    allowed_styles = [
        'float', 'margin', 'margin-left', 'margin-right', 'width', 'height',
        'border-style', 'border-width', 'background', 'border', 'padding'
    ]

    cleaned = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, styles=allowed_styles)
    return cleaned


# ADMIN-ONLY DECORATOR
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin" and current_user.role != "owner":
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/dashboard/<choice>')
@login_required
@admin_only
def admin(choice):
    all_users = []
    if choice == 'all':
        all_users = db.session.query(User).all()
    if choice == 'admins':
        all_users = db.session.query(User).filter_by(role='admin').all()
    if choice == 'users':
        all_users = db.session.query(User).filter_by(role='user').all()
    return render_template('admin-panel.html', users=all_users)


@app.route("/dashboard/<int:user_id>/delete")
@login_required
@admin_only
def remove_from_admin(user_id):
    admin_to_delete = db.session.query(User).get(user_id)
    admin_to_delete.role = "user"
    db.session.commit()

    return redirect(url_for('admin', choice='all'))


@app.route("/dashboard/<int:user_id>/add")
@login_required
@admin_only
def make_admin(user_id):
    admin_to_make = db.session.query(User).get(user_id)
    admin_to_make.role = "admin"
    db.session.commit()

    return redirect(url_for('admin', choice='all'))


@app.route("/dashboard/<int:user_id>/remove")
@login_required
@admin_only
def delete_user(user_id):
    blog_to_delete = BlogPost.query.filter_by(author_id=user_id).all()
    for blog in blog_to_delete:
        db.session.delete(blog)
        db.session.commit()

    comment_to_delete = Comment.query.filter_by(author_id=user_id).all()
    for comment in comment_to_delete:
        db.session.delete(comment)
        db.session.commit()

    user_to_delete = db.session.query(User).get(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect(url_for('admin', choice='all'))


@app.route("/new", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    page_heading_msg = 'New Post'
    new_post_form = CreatePostForm()
    if new_post_form.validate_on_submit():
        new_post = BlogPost(
            title=new_post_form.title.data,
            subtitle=new_post_form.subtitle.data,
            body=sanitize_html(new_post_form.body.data),
            img_url=new_post_form.img_url.data,
            img_src=new_post_form.img_src.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()

        comment_form = CommentForm()
        requested_post = BlogPost.query.order_by(BlogPost.id)[-1]

        return render_template('post.html', blog=requested_post, form=comment_form)

    return render_template("make-post.html", form=new_post_form, MSG=page_heading_msg)


@app.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    blog = db.session.query(BlogPost).get(post_id)
    page_heading_msg = f'You are editing "{blog.title}"'
    edit_form = CreatePostForm(
        title=blog.title,
        subtitle=blog.subtitle,
        author=blog.author,
        img_url=blog.img_url,
        img_src=blog.img_src,
        body=blog.body
    )
    if edit_form.validate_on_submit():
        blog.title = edit_form.title.data
        blog.subtitle = edit_form.subtitle.data
        blog.img_url = edit_form.img_url.data
        blog.img_src = edit_form.img_src.data
        blog.body = sanitize_html(edit_form.body.data)
        db.session.commit()

        requested_post = db.session.query(BlogPost).get(post_id)
        comment_form = CommentForm()

        return render_template('post.html', blog=requested_post, form=comment_form)

    return render_template("make-post.html", form=edit_form, MSG=page_heading_msg)


@app.route("/<int:post_id>/delete")
@login_required
@admin_only
def delete_post(post_id):
    blog_to_delete = db.session.query(BlogPost).get(post_id)
    db.session.delete(blog_to_delete)
    db.session.commit()

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
