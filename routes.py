import os
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, extract
from werkzeug.security import generate_password_hash

from app import db
from models import User, Workout, Exercise, WorkoutExercise, Goal
from forms import (LoginForm, RegisterForm, WorkoutForm, ExerciseSearchForm, 
                  WorkoutExerciseForm, GoalForm, ProfileForm)

def init_routes(app):
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('login'))
            
        return render_template('register.html', form=form)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
            
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Login failed. Please check your email and password.', 'danger')
                
        return render_template('login.html', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Get the start and end dates for the current week
        today = datetime.utcnow().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Weekly summary data
        workouts_count = Workout.query.filter(
            Workout.user_id == current_user.id,
            Workout.date >= start_of_week,
            Workout.date <= end_of_week
        ).count()
        
        # Calculate total workout time
        total_duration = db.session.query(func.sum(Workout.duration)).filter(
            Workout.user_id == current_user.id,
            Workout.date >= start_of_week,
            Workout.date <= end_of_week
        ).scalar() or 0
        
        # Calculate total calories
        total_calories = db.session.query(func.sum(Workout.calories)).filter(
            Workout.user_id == current_user.id,
            Workout.date >= start_of_week,
            Workout.date <= end_of_week
        ).scalar() or 0
        
        # Format duration as hours and minutes
        hours, minutes = divmod(total_duration, 60)
        duration_formatted = f"{hours}h {minutes}m"
        
        # Get recent workouts
        recent_workouts = Workout.query.filter_by(
            user_id=current_user.id
        ).order_by(Workout.date.desc()).limit(5).all()
        
        # Get active goals
        goals = Goal.query.filter_by(
            user_id=current_user.id,
            completed=False
        ).order_by(Goal.end_date).limit(3).all()
        
        return render_template(
            'dashboard.html',
            workouts_count=workouts_count,
            duration_formatted=duration_formatted,
            total_calories=total_calories,
            recent_workouts=recent_workouts,
            goals=goals,
            date=datetime.utcnow()
        )
    
    @app.route('/workouts')
    @login_required
    def workouts():
        page = request.args.get('page', 1, type=int)
        workouts = Workout.query.filter_by(
            user_id=current_user.id
        ).order_by(Workout.date.desc()).paginate(page=page, per_page=10)
        
        return render_template('workouts.html', workouts=workouts)
    
    @app.route('/workouts/add', methods=['GET', 'POST'])
    @login_required
    def add_workout():
        form = WorkoutForm()
        if form.validate_on_submit():
            workout = Workout(
                user_id=current_user.id,
                name=form.name.data,
                duration=form.duration.data,
                calories=form.calories.data,
                date=form.date.data,
                notes=form.notes.data
            )
            db.session.add(workout)
            db.session.commit()
            
            flash('Workout added successfully!', 'success')
            return redirect(url_for('workouts'))
            
        return render_template('add_workout.html', form=form, title='Add Workout')
    
    @app.route('/workouts/<int:workout_id>')
    @login_required
    def view_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        
        # Check if the workout belongs to the current user
        if workout.user_id != current_user.id:
            flash('You do not have permission to view this workout.', 'danger')
            return redirect(url_for('workouts'))
            
        exercises = WorkoutExercise.query.filter_by(workout_id=workout.id).all()
        
        return render_template('view_workout.html', workout=workout, exercises=exercises)
    
    @app.route('/workouts/<int:workout_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        
        # Check if the workout belongs to the current user
        if workout.user_id != current_user.id:
            flash('You do not have permission to edit this workout.', 'danger')
            return redirect(url_for('workouts'))
            
        form = WorkoutForm()
        
        if form.validate_on_submit():
            workout.name = form.name.data
            workout.duration = form.duration.data
            workout.calories = form.calories.data
            workout.date = form.date.data
            workout.notes = form.notes.data
            
            db.session.commit()
            flash('Workout updated successfully!', 'success')
            return redirect(url_for('view_workout', workout_id=workout.id))
            
        elif request.method == 'GET':
            form.name.data = workout.name
            form.duration.data = workout.duration
            form.calories.data = workout.calories
            form.date.data = workout.date
            form.notes.data = workout.notes
            
        return render_template('add_workout.html', form=form, title='Edit Workout')
    
    @app.route('/workouts/<int:workout_id>/delete', methods=['POST'])
    @login_required
    def delete_workout(workout_id):
        workout = Workout.query.get_or_404(workout_id)
        
        # Check if the workout belongs to the current user
        if workout.user_id != current_user.id:
            flash('You do not have permission to delete this workout.', 'danger')
            return redirect(url_for('workouts'))
            
        db.session.delete(workout)
        db.session.commit()
        
        flash('Workout deleted successfully!', 'success')
        return redirect(url_for('workouts'))
    
    @app.route('/exercises')
    @login_required
    def exercises():
        form = ExerciseSearchForm()
        
        # Get filters from query parameters
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        # Query exercises with filters
        query = Exercise.query
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(Exercise.name.ilike(search_term) | 
                                Exercise.description.ilike(search_term))
        
        if category:
            query = query.filter_by(category=category)
            
        exercises = query.order_by(Exercise.name).all()
        
        return render_template('exercises.html', exercises=exercises, form=form)
    
    @app.route('/goals')
    @login_required
    def goals():
        active_goals = Goal.query.filter_by(
            user_id=current_user.id,
            completed=False
        ).order_by(Goal.end_date).all()
        
        completed_goals = Goal.query.filter_by(
            user_id=current_user.id,
            completed=True
        ).order_by(Goal.end_date.desc()).all()
        
        return render_template('goals.html', active_goals=active_goals, completed_goals=completed_goals)
    
    @app.route('/goals/add', methods=['GET', 'POST'])
    @login_required
    def add_goal():
        form = GoalForm()
        
        if form.validate_on_submit():
            goal = Goal(
                user_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                target_value=form.target_value.data,
                goal_type=form.goal_type.data,
                end_date=form.end_date.data
            )
            
            db.session.add(goal)
            db.session.commit()
            
            flash('Goal added successfully!', 'success')
            return redirect(url_for('goals'))
            
        return render_template('add_goal.html', form=form, title='Add Goal')
    
    @app.route('/goals/<int:goal_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_goal(goal_id):
        goal = Goal.query.get_or_404(goal_id)
        
        # Check if the goal belongs to the current user
        if goal.user_id != current_user.id:
            flash('You do not have permission to edit this goal.', 'danger')
            return redirect(url_for('goals'))
            
        form = GoalForm()
        
        if form.validate_on_submit():
            goal.title = form.title.data
            goal.description = form.description.data
            goal.target_value = form.target_value.data
            goal.goal_type = form.goal_type.data
            goal.end_date = form.end_date.data
            
            db.session.commit()
            flash('Goal updated successfully!', 'success')
            return redirect(url_for('goals'))
            
        elif request.method == 'GET':
            form.title.data = goal.title
            form.description.data = goal.description
            form.target_value.data = goal.target_value
            form.goal_type.data = goal.goal_type
            form.end_date.data = goal.end_date
            
        return render_template('add_goal.html', form=form, title='Edit Goal')
    
    @app.route('/goals/<int:goal_id>/update-progress', methods=['POST'])
    @login_required
    def update_goal_progress(goal_id):
        goal = Goal.query.get_or_404(goal_id)
        
        # Check if the goal belongs to the current user
        if goal.user_id != current_user.id:
            flash('You do not have permission to update this goal.', 'danger')
            return redirect(url_for('goals'))
            
        current_value = request.form.get('current_value', type=float)
        
        if current_value is not None:
            goal.current_value = current_value
            
            # Check if goal is completed
            if goal.current_value >= goal.target_value:
                goal.completed = True
                
            db.session.commit()
            flash('Goal progress updated successfully!', 'success')
            
        return redirect(url_for('goals'))
    
    @app.route('/goals/<int:goal_id>/delete', methods=['POST'])
    @login_required
    def delete_goal(goal_id):
        goal = Goal.query.get_or_404(goal_id)
        
        # Check if the goal belongs to the current user
        if goal.user_id != current_user.id:
            flash('You do not have permission to delete this goal.', 'danger')
            return redirect(url_for('goals'))
            
        db.session.delete(goal)
        db.session.commit()
        
        flash('Goal deleted successfully!', 'success')
        return redirect(url_for('goals'))
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm()
        
        if form.validate_on_submit():
            # Check if username is being changed and is available
            if form.username.data != current_user.username:
                existing_user = User.query.filter_by(username=form.username.data).first()
                if existing_user:
                    flash('Username already taken. Please choose a different one.', 'danger')
                    return render_template('profile.html', form=form)
            
            # Check if email is being changed and is available
            if form.email.data != current_user.email:
                existing_user = User.query.filter_by(email=form.email.data).first()
                if existing_user:
                    flash('Email already registered. Please use a different one.', 'danger')
                    return render_template('profile.html', form=form)
            
            # Update username and email
            current_user.username = form.username.data
            current_user.email = form.email.data
            
            # Change password if provided
            if form.new_password.data:
                if not current_user.check_password(form.current_password.data):
                    flash('Current password is incorrect.', 'danger')
                    return render_template('profile.html', form=form)
                
                current_user.set_password(form.new_password.data)
            
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile'))
            
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            
        return render_template('profile.html', form=form)
    
    @app.route('/initialize-db')
    def initialize_db():
        # Only run in development mode
        if not app.debug:
            return "This route is only available in debug mode", 403
            
        # Initialize exercise library if it's empty
        if Exercise.query.count() == 0:
            exercises = [
                {
                    'name': 'Bench Press',
                    'description': 'A compound chest exercise performed on a bench with a barbell.',
                    'category': 'chest',
                    'muscles_targeted': 'Chest, Triceps, Shoulders',
                    'image_url': 'bench-press'
                },
                {
                    'name': 'Deadlift',
                    'description': 'A compound exercise that works multiple muscle groups including the back, legs, and core.',
                    'category': 'back',
                    'muscles_targeted': 'Back, Hamstrings, Glutes, Core',
                    'image_url': 'deadlift'
                },
                {
                    'name': 'Squat',
                    'description': 'A compound lower body exercise that targets the quadriceps, hamstrings, and glutes.',
                    'category': 'legs',
                    'muscles_targeted': 'Quads, Glutes, Core',
                    'image_url': 'squat'
                },
                {
                    'name': 'Pull-ups',
                    'description': 'A bodyweight exercise that targets the back and biceps.',
                    'category': 'back',
                    'muscles_targeted': 'Back, Biceps, Forearms',
                    'image_url': 'pull-ups'
                },
                {
                    'name': 'Push-ups',
                    'description': 'A bodyweight exercise that targets the chest, shoulders, and triceps.',
                    'category': 'chest',
                    'muscles_targeted': 'Chest, Shoulders, Triceps, Core',
                    'image_url': 'push-ups'
                },
                {
                    'name': 'Shoulder Press',
                    'description': 'An upper body exercise that targets the shoulders and triceps.',
                    'category': 'shoulders',
                    'muscles_targeted': 'Shoulders, Triceps',
                    'image_url': 'shoulder-press'
                },
                {
                    'name': 'Bicep Curls',
                    'description': 'An isolation exercise that targets the biceps.',
                    'category': 'arms',
                    'muscles_targeted': 'Biceps',
                    'image_url': 'bicep-curls'
                },
                {
                    'name': 'Tricep Extensions',
                    'description': 'An isolation exercise that targets the triceps.',
                    'category': 'arms',
                    'muscles_targeted': 'Triceps',
                    'image_url': 'tricep-extensions'
                },
                {
                    'name': 'Plank',
                    'description': 'A core exercise that targets the abdominals and lower back.',
                    'category': 'core',
                    'muscles_targeted': 'Core, Shoulders',
                    'image_url': 'plank'
                },
                {
                    'name': 'Lunges',
                    'description': 'A lower body exercise that targets the quadriceps, hamstrings, and glutes.',
                    'category': 'legs',
                    'muscles_targeted': 'Quads, Hamstrings, Glutes',
                    'image_url': 'lunges'
                },
                {
                    'name': 'Running',
                    'description': 'A cardiovascular exercise that targets the entire body.',
                    'category': 'cardio',
                    'muscles_targeted': 'Full Body',
                    'image_url': 'running'
                },
                {
                    'name': 'Cycling',
                    'description': 'A cardiovascular exercise that targets the lower body.',
                    'category': 'cardio',
                    'muscles_targeted': 'Legs',
                    'image_url': 'cycling'
                }
            ]
            
            for exercise_data in exercises:
                exercise = Exercise(**exercise_data)
                db.session.add(exercise)
                
            db.session.commit()
            
            return "Exercise library initialized successfully!"
        else:
            return "Database already contains exercises."

    @app.context_processor
    def inject_today():
        return {'today': datetime.utcnow()}
