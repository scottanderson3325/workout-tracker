from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'workouts.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        workouts = {
            "Monday": request.form.get("monday"),
            "Tuesday": request.form.get("tuesday"),
            "Wednesday": request.form.get("wednesday"),
            "Thursday": request.form.get("thursday"),
            "Friday": request.form.get("friday"),
            "Saturday": request.form.get("saturday"),
            "Sunday": request.form.get("sunday"),
        }
        
        # Save to database
        for day, workout_type in workouts.items():
            if workout_type:    # Only save non-empty days
                db.session.add(Workout(day=day, workout_type=workout_type))
        db.session.commit()
        
        return render_template("schedule.html", workouts=workouts)

    return render_template("schedule.html", workouts={})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)