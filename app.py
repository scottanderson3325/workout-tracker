from flask import Flask, render_template, request, redirect
from models import db, Workout, Exercise
from datetime import datetime, timedelta

import os

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

# View Workout Page
@app.route('/view/<int:workout_id>')
def view_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return render_template('view_workout.html', workout=workout)

# Schedule Page
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        name = request.form.get('name')
        date_str = request.form.get('date')
        repeat_weekly = bool(request.form.get('repeat_weekly'))  # "on" becomes True, None becomes False
        repeat_weeks = int(request.form.get('repeat_weeks') or 1)  # defaults to 1 if not set

        if name and date_str:
            workout_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_of_week = workout_date.strftime('%A')
            
            if repeat_weekly:
                for i in range(repeat_weeks):
                    repeated_date = workout_date + timedelta(weeks=i)
                    day_of_week = repeated_date.strftime('%A')

                    new_workout = Workout(
                        name=name,
                        date=repeated_date,
                        day_of_week=day_of_week,
                        repeat_weekly=True
                    )
                    db.session.add(new_workout)
            else:
                # Just one workout, no repeats
                new_workout = Workout(
                    name=name,
                    date=workout_date,
                    day_of_week=day_of_week,
                    repeat_weekly=False
                )
                db.session.add(new_workout)


            db.session.commit() # Commit once after
            return redirect('/schedule') # Redirect once, after commit

    # Handling week navigation
    week_offset = int(request.args.get('week_offset',0))
    
    # Adjust the start of the week based on the offset
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() < 6 else 0)
    start_of_week += timedelta(weeks=week_offset)
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Get workouts in current week
    workouts = Workout.query.filter(Workout.date.in_(week_dates)).all()

    # Group workouts by day
    week_schedule = {date.strftime('%A'): [] for date in week_dates}
    for workout in workouts:
        week_schedule[workout.day_of_week].append(workout)

    return render_template(
        'schedule.html',
        week_schedule=week_schedule,
        start_of_week=start_of_week,
        end_of_week=week_dates[-1],
        week_offset=week_offset
    )
    
@app.route('/exercises')
def view_exercises():
    exercises = Exercise.query.all()
    return render_template('exercises.html', exercises=exercises)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
