from app import app
from models import db, Workout

with app.app_context():
    workouts = Workout.query.all()

    if not workouts:
        print("No workouts found.")
    else:
        print("Saved Workouts:")
        for workout in workouts:
            print(f"{workout.id}: {workout.name} on {workout.day_of_week} ({workout.date}) - Repeat Weekly: {workout.repeat_weekly}")
