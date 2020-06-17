from app import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,SubmitField,FloatField, BooleanField, PasswordField,RadioField, IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length,Email,EqualTo

class RegistrationForm(FlaskForm):
    username =StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    firstname =StringField('Firstname',validators=[DataRequired(),Length(min=2,max=20)])
    lastname =StringField('Lastname',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username =StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    #email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    

class UpdateAccountForm(FlaskForm):
    # username =StringField('Username')
    # email = StringField('Email',validators=[Email()])
    age =  IntegerField('Age',validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female'),('Bisexual','Other')])
    # picture = FileField('Upload picture',validators=[FileField(['jpg','png'])])
    sexualPreference = RadioField('SexualPreference',choices=[('Male','Male'),('Female','Female'),('Bisexual','Bisexual')])
    bio = TextAreaField('Biography',validators=[DataRequired(),Length(min=2,max=100)])
    interest = StringField('Interest',validators=[DataRequired(),Length(min=2,max=100)])
    submit = SubmitField('Update')

class UploadsForm(FlaskForm):
    username =StringField('Username')
    # firstname = StringField('Firstname')
    # lastname = StringField("Lastname")
    email = StringField('Email',validators=[Email()])
    # age =  IntegerField('Age')
    # gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female'),('Bisexual','Other')])
    # sexualPreference = RadioField('SexualPreference',choices=[('Male','Male'),('Female','Female'),('Bisexual','Bisexual')])
    picture = FileField('Upload picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')

class MessageForm(FlaskForm):
    username = StringField('Username')
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('send')