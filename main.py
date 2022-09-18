from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, Markup, render_template, redirect, url_for, request, flash, abort, send_from_directory
from forms import ContactForm, CreatePostForm, RegisterForm, LoginForm, CommentForm, CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar
from functools import wraps
from sqlalchemy import exc
from datetime import date
import smtplib
import bleach
import os


# CONFIGURE FLASK
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.environ.get("CSRF_KEY")

# CONFIGURE BOOTSTRAP, CKEDITOR, GRAVATAR
ckeditor = CKEditor(app)
bootstrap = Bootstrap(app)
gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)

# CONNECT TO DATABASE, CONFIGURE SQLALCHEMY
db_uri = os.environ.get("DATABASE_URL")
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(db_uri, "sqlite:///main.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# SECRET CREDENTIALS
sender_email = os.environ.get("EMAIL")
sender_password = os.environ.get("PASSWORD")
owner_email = os.environ.get("OWNER_EMAIL")


# CONFIGURE TABLES IN DATABASE
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(256))
    role = db.Column(db.String(256))

    blog_posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    img_src = db.Column(db.String(255), nullable=True)

    author = relationship("User", back_populates="blog_posts")
    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(255), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    comment_author = relationship("User", back_populates="comments")
    parent_post = relationship("BlogPost", back_populates="comments")


db.create_all()
