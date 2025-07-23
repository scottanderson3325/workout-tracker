from app import app
from models import db, Workout, Exercise

with app.app_context():
    workouts = Workout.query.all()

    if not workouts:
        print("No workouts found.")
    else:
        print("Saved Workouts:")
        for workout in workouts:
            print(f"{workout.id}: {workout.name} on {workout.day_of_week} ({workout.date}) - Repeat Weekly: {workout.repeat_weekly}")

    exercises = Exercise.query.all()
    
    if not exercises:
        print("No exercises found.")
    else:
        print("Saved Exercises")
        for exercise in exercises:
            print(f"{exercise.id}: {exercise.name} - {exercise.instructions}")
    