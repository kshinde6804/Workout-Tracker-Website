from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Exercise, WorkoutLog, Workout
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    exercises = Exercise.query.all()
    return render_template('index.html', exercises=exercises)

@bp.route('/add_exercise', methods=['GET', 'POST'])
def add_exercise():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            existing_exercise = Exercise.query.filter_by(name=name).first()
            if existing_exercise:
                flash('Exercise already exists!')
                return redirect(url_for('main.add_exercise'))
            else:
                new_exercise = Exercise(name=name)
                db.session.add(new_exercise)
                db.session.commit()
                flash('Exercise added successfully!')
                return redirect(url_for('main.index'))
    return render_template('add_exercise.html')

@bp.route('/test_link', methods=['GET', 'POST'])
def test_link():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            new_exercise = Exercise(name=name)
            db.session.add(new_exercise)
            db.session.commit()
            flash('TEST TEST TEST!')
            return redirect(url_for('main.index'))
    return render_template('test_link.html')

@bp.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if request.method == 'POST':
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date object
        new_workout = Workout(date=date_obj)
        db.session.add(new_workout)
        db.session.commit()

        exercise_ids = request.form.getlist('exercise')
        sets = request.form.getlist('sets')
        reps = request.form.getlist('reps')
        weights = request.form.getlist('weight')

        for exercise_id, set_count, rep, weight in zip(exercise_ids, sets, reps, weights):
            log = WorkoutLog(exercise_id=exercise_id, sets=set_count, reps=rep, weight=weight, workout_id=new_workout.id)
            db.session.add(log)

        db.session.commit()
        flash('Workout logged successfully!')
        return redirect(url_for('main.index'))
    exercises = Exercise.query.all()
    return render_template('log_workout.html', exercises=exercises)

@bp.route('/exercise_catalog', methods=['GET', 'POST'])
def exercise_catalog():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            existing_exercise = Exercise.query.filter_by(name=name).first()
            if existing_exercise:
                flash('Exercise already exists!')
            else:
                new_exercise = Exercise(name=name)
                db.session.add(new_exercise)
                db.session.commit()
                flash('Exercise added successfully!')
        return redirect(url_for('main.exercise_catalog'))
    exercises = Exercise.query.all()
    return render_template('exercise_catalog.html', exercises=exercises)

@bp.route('/delete_exercise/<int:exercise_id>', methods=['POST'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        flash('Exercise deleted successfully!')
    else:
        flash('Exercise not found.')
    return redirect(url_for('main.exercise_catalog'))

@bp.route('/workouts', methods=['GET', 'POST'])
def workouts():
    workouts = Workout.query.all()
    return render_template('workouts.html', workouts=workouts)
