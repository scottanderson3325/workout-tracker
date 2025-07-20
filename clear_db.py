from app import db, Workout, app

with app.app_context():
    num_deleted = Workout.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} workouts.")
