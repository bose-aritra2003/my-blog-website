from flask import Markup
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, URL


def makeStrong(text):
    return Markup(f'<strong>{text}</strong>')


# FORM FOR CREATING A BLOG POST
class ContactForm(FlaskForm):
    name = StringField(makeStrong("Name"), validators=[DataRequired()])
    email = StringField(makeStrong("Email"), validators=[DataRequired()])
    subject = StringField(makeStrong("Subject"), validators=[DataRequired()])
    message = TextAreaField(makeStrong("Message"), validators=[DataRequired()])
    submit = SubmitField("Send")


class CreatePostForm(FlaskForm):
    title = StringField(makeStrong("Blog Post Title"), validators=[DataRequired()])
    subtitle = StringField(makeStrong("Subtitle"), validators=[DataRequired()])
    img_url = StringField(makeStrong("Blog Image URL"), validators=[DataRequired(), URL()])
    img_src = StringField(makeStrong("Blog Image Source"), validators=[DataRequired()])
    body = CKEditorField(makeStrong("Blog Content"), validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# FORM FOR CREATING AN USER
class RegisterForm(FlaskForm):
    email = StringField(makeStrong("Email"), validators=[DataRequired()])
    password = PasswordField(makeStrong("Password"), validators=[DataRequired()])
    name = StringField(makeStrong("Name"), validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# FORM FOR LOGGING IN
class LoginForm(FlaskForm):
    email = StringField(makeStrong("Email"), validators=[DataRequired()])
    password = PasswordField(makeStrong("Password"), validators=[DataRequired()])
    submit = SubmitField('Let me in!')


# GET EMAIL FORM
class EmailForm(FlaskForm):
    email = StringField(makeStrong("Email"), validators=[DataRequired()])
    submit = SubmitField("Confirm")


# VERIFY FORM
class OTPForm(FlaskForm):
    otp = StringField(makeStrong("Verification Code"), validators=[DataRequired()])
    submit = SubmitField("Verify")


# RESET PASSWORD FORM
class ResetPasswordForm(FlaskForm):
    password = PasswordField(makeStrong("New Password"), validators=[DataRequired()])
    submit = SubmitField("Submit")


# FORM FOR CREATING A COMMENT
class CommentForm(FlaskForm):
    text = TextAreaField(makeStrong("Comment"), validators=[DataRequired()])
    submit = SubmitField("Submit")
