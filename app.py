from flask import Flask, render_template, request, redirect, url_for
from models import db, Workout, Exercise, WorkoutExercise
from datetime import datetime, timedelta

import os
import json

app = Flask(__name__)

# Configure DB path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'workout_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db (don't re-assign!)
db.init_app(app)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view/<int:workout_id>')
def view_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)

    workout_exercises = (
        db.session.query(WorkoutExercise)
        .filter_by(workout_id=workout.id)
        .join(Exercise)
        .all()
    )

    print(f"📋 Found {len(workout_exercises)} exercises for Workout ID {workout.id}")  # 👈 ADD THIS

    all_exercises = Exercise.query.all()
    return render_template(
        'view_workout.html',
        workout=workout,
        workout_exercises=workout_exercises,
        all_exercises=all_exercises
    )

# 🔄 Route: Add Exercises to a Workout
# -------------------------------------
# This route is triggered when the user saves their workout with new exercises.
# It takes a list of selected exercise IDs from the form, adds them to the 
# WorkoutExercise table, and then redirects back to the workout view page.

@app.route('/view/<int:workout_id>/add_exercises', methods=['POST'])
def add_exercises_to_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    selected_ids = request.form.get('exercise_ids')

    print("📨 Raw POST data (selected_exercises):", selected_ids)  # 👈 ADD THIS

    if selected_ids:
        try:
            exercise_ids = json.loads(selected_ids)
            print("✅ Parsed exercise_ids:", exercise_ids)  # 👈 ADD THIS

            for ex_id in exercise_ids:
                print(f"🔄 Adding Exercise ID {ex_id} to Workout ID {workout.id}")  # 👈 ADD THIS
                workout_exercise = WorkoutExercise(
                    workout_id=workout.id,
                    exercise_id=int(ex_id)
                )
                db.session.add(workout_exercise)

            db.session.commit()
            print("💾 Commit successful")  # 👈 ADD THIS

        except Exception as e:
            db.session.rollback()
            print("❌ Error saving exercises:", e)

    return redirect(url_for('view_workout', workout_id=workout.id))

# 📅 Route: Weekly Schedule Page
# -------------------------------
# This route serves two purposes:
# 1. Handle POST requests to create a new workout (possibly repeating weekly).
# 2. Handle GET requests to display a calendar week of workouts, grouped by day.

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    # 📝 Handle Workout Creation (Form Submission)
    if request.method == 'POST':
        # Extract form values
        name = request.form.get('name')  # Name of the workout
        date_str = request.form.get('date')  # The selected date as a string
        repeat_weekly = bool(request.form.get('repeat_weekly'))  # Checkbox toggle
        repeat_weeks = int(request.form.get('repeat_weeks') or 1)  # Default to 1 if blank

        if name and date_str:
            # Parse the workout date and derive the day of the week
            workout_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_of_week = workout_date.strftime('%A')
            
            if repeat_weekly:
                # Loop through the number of repeat weeks
                for i in range(repeat_weeks):
                    repeated_date = workout_date + timedelta(weeks=i)
                    day_of_week = repeated_date.strftime('%A')

                    # Create a new Workout entry for each repeated week
                    new_workout = Workout(
                        name=name,
                        date=repeated_date,
                        day_of_week=day_of_week,
                        repeat_weekly=True
                    )
                    db.session.add(new_workout)
            else:
                # Single workout entry with no repeats
                new_workout = Workout(
                    name=name,
                    date=workout_date,
                    day_of_week=day_of_week,
                    repeat_weekly=False
                )
                db.session.add(new_workout)

            # Save all new workout(s) to the database
            db.session.commit()
            return redirect('/schedule')  # Refresh the page after form submit

    # 📆 Handle GET Request: Show Current Week’s Workouts

    # Get the current offset for week navigation (e.g., next/previous week)
    week_offset = int(request.args.get('week_offset', 0))
    
    # Calculate the start of the current week (Sunday)
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() < 6 else 0)
    start_of_week += timedelta(weeks=week_offset)
    
    # Generate all 7 dates in the selected week
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Query all workouts scheduled for the current week
    workouts = Workout.query.filter(Workout.date.in_(week_dates)).all()

    # Group workouts by the day of the week they fall on
    week_schedule = {date.strftime('%A'): [] for date in week_dates}
    for workout in workouts:
        week_schedule[workout.day_of_week].append(workout)

    # Render the weekly calendar view with all relevant data
    return render_template(
        'schedule.html',
        week_schedule=week_schedule,
        start_of_week=start_of_week,
        end_of_week=week_dates[-1],
        week_offset=week_offset
    )

    
#-----------------------------------------------------------------------------------------------
    
@app.route('/exercises')
def view_exercises():
    exercises = Exercise.query.all()
    return render_template('exercises.html', exercises=exercises)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
