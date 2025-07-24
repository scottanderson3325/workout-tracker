# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    day_of_week = db.Column(db.String(10))
    repeat_weekly = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    instructions = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(255), nullable=True)

    primary_muscle = db.Column(db.String(100), nullable=False)
    secondary_muscles = db.Column(db.String(255), nullable=True)   # comma-separated
    stabilizers = db.Column(db.String(255), nullable=True)         # comma-separated

    def __repr__(self):
        return f"<Exercise {self.name}>"
    
class WorkoutExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)

    set_number = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight_used = db.Column(db.Float)
    order = db.Column(db.Integer)  # for UI reordering (optional)

    exercise = db.relationship('Exercise')  # so you can do .exercise.name

    