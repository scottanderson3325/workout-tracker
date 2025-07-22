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

    def __repr__(self):
        return f"<Exercise {self.name}>"
