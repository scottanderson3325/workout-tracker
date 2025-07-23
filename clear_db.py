from app import app
from models import db, Workout, Exercise

with app.app_context():
    
    num_deleted = Workout.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} workouts.")

    num_deleted = Exercise.query.delete()
    db.session.commit()
    print(f"Deleted {num_deleted} exercises.")