from app import db, Workout, app

with app.app_context():
    workouts = Workout.query.all()

    if not workouts:
        print("No workouts found.")
    else:
        print("Saved Workouts:")
        for workout in workouts:
            print(f"{workout.id}: {workout.day} — {workout.workout_type}")
