# Air Blogs
<img src="https://raw.githubusercontent.com/bose-aritra2003/my-blog-website/master/static/assets/favicon.ico"></img>

* https://air-blogs.onrender.com
* An End-to-End application, managed from development through deployment to production.


## Functionality
* Users need to register/login in order to comment on posts.
* New users' email addresses are verified before they are registered.
* Passwords are securely encoded with PBKDF2-SHA-256 encryption method of the werkzeug.security package.
* User authentication is done with a flask_login object
* Only Admin users and the Owner can create and delete posts.
* Users can get in contact with the the owner(me) by sending a message through the contact section, which gets transferred via email over a SMTP client session object.
* User also has the option to reset their password in case they forget.
* The App makes use of CKEditor (for creating posts); a WYSIWYG rich text editor which enables writing content directly inside of web pages/online applications.
* (Production) WSGI server is setup with Gunicorn to run the Live Python Application on Heroku. PostgreSQL database is used for production.
* (Development) Development and testing is done locally with a SQLite database.

## Technology used

* Python
* Bootstrap 5
* Flask Web Framework 
* PostgreSQL
* Jinja2
* Werkzeug Security
* WTForms

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements for air-blogs.
```bash
pip install -r requirements.txt
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Sample Images
![](https://i.imgur.com/Ww0JLLl.png)
<br>
![](https://i.imgur.com/t6TPozj.png)
<br>
![](https://i.imgur.com/3cPo1Jm.png)
<br>
![](https://i.imgur.com/1sloeig.png)
<br>
![](https://i.imgur.com/UFXEFNZ.png)
<br>
![](https://i.imgur.com/Y3obCnU.png)
<br>
![](https://i.imgur.com/0EP1Xkx.png)
<br>
![](https://i.imgur.com/9Ky9ZJq.png)

