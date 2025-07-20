from flask import Flask, render_template, request, redirect
from models import db, Workout
from datetime import datetime, timedelta

import os

app = Flask(__name__)

# Configure DB path
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'workouts.db')
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
        repeat_weekly = bool(request.form.get('repeat_weekly'))

        if name and date_str:
            workout_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_of_week = workout_date.strftime('%A')

            new_workout = Workout(
                name=name,
                date=workout_date,
                day_of_week=day_of_week,
                repeat_weekly=repeat_weekly
            )
            db.session.add(new_workout)
            db.session.commit()
            return redirect('/schedule')

    # Get current week (Sunday–Saturday)
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday() + 1 if today.weekday() < 6 else 0)
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Get workouts in current week
    workouts = Workout.query.filter(Workout.date.in_(week_dates)).all()

    # Group workouts by day
    week_schedule = {date.strftime('%A'): [] for date in week_dates}
    for workout in workouts:
        week_schedule[workout.day_of_week].append(workout)

    return render_template('schedule.html', week_schedule=week_schedule)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
