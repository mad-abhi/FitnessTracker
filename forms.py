from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField, IntegerField
from wtforms import FloatField, SelectField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class WorkoutForm(FlaskForm):
    name = StringField('Workout Name', validators=[DataRequired()])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    calories = IntegerField('Calories Burned', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Workout')

class ExerciseSearchForm(FlaskForm):
    search = StringField('Search Exercises', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('arms', 'Arms'),
        ('shoulders', 'Shoulders'),
        ('legs', 'Legs'),
        ('core', 'Core'),
        ('cardio', 'Cardio')
    ], validators=[Optional()])
    submit = SubmitField('Search')

class WorkoutExerciseForm(FlaskForm):
    exercise_id = HiddenField('Exercise ID', validators=[DataRequired()])
    sets = IntegerField('Sets', validators=[Optional()])
    reps = IntegerField('Reps', validators=[Optional()])
    weight = FloatField('Weight (lbs)', validators=[Optional()])
    duration = IntegerField('Duration (seconds)', validators=[Optional()])
    submit = SubmitField('Add to Workout')

class GoalForm(FlaskForm):
    title = StringField('Goal Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    target_value = FloatField('Target Value', validators=[DataRequired()])
    goal_type = SelectField('Goal Type', choices=[
        ('weight', 'Weight Goal'),
        ('workouts', 'Number of Workouts'),
        ('calories', 'Calories Burned')
    ], validators=[DataRequired()])
    end_date = DateField('Target Date', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Save Goal')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', 
                                     validators=[Optional(), EqualTo('new_password')])
    submit = SubmitField('Update Profile')
