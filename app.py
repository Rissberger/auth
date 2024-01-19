from flask import Flask, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm  # Make sure LoginForm is defined in forms.py
from models import User  # Ensure User model is defined in models.py
from extensions import db  # Assuming db initialization is in extensions.py

app = Flask(__name__)

# Configuration settings
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///table"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

db.init_app(app)

# ... [rest of your app configuration and setup] ...

@app.route('/')
def index():
    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('secret'))  # Redirect to /secret
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
       username = form.username.data
       password = form.password.data

       user = User.authenticate(username, password)
       if user:
        session['username'] = user.username
        return redirect(f"/users/{user.username}")
       else:
        form.username.errors = ["invalid user or pass"]
        return render_template("users/login.html", form=form)
    return render_template('users/login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/users.<username>')
def username(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.p('username')

    return redirect('/login')

@app.route('/users/<username>/feedback/new' methods=["GET", "POST"])
def new_feed(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    else:
        return render_template("feedback/new.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feed(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f"/users/{feedback.username}")
    
    return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feed(feedback_id):

    feed = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.add(feedback)
        db.session.commit()
    return redirect(f'/users/{feedback.username}')
    


@app.route('/secret')
def secret():
    return "You made it!"
    
if __name__ == "__main__":
    app.run(debug=True)
