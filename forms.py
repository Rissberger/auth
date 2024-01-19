from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Register')

class Login(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), length(min=1, max=20)],
    )
    password = PasswordField("Password", validators=[InputRequired(), length(min=6, max=55)],
    )

class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired(), length(max=100)],
    )
    content = StringField("Content", validators=[InputRequired()],
    )

class DeleteForm(FlaskForm):
