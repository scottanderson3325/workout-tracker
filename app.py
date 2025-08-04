"""
Main Flask application for the Workout Tracker.

This module defines the web interface for the project. Routes are organized
in the order a user might naturally navigate the site:
    1. Home page
    2. Weekly schedule
    3. Viewing a single workout
    4. Adding exercises to a workout
    5. Updating sets/reps/weights
    6. Deleting an exercise from a workout
    7. Listing all exercises
"""

from datetime import datetime, timedelta
import json
import os

from flask import abort, Flask, render_template, request, redirect, url_for

from models import db, Workout, Exercise, WorkoutExercise


# -----------------------------------------------------------------------------
# Application setup
# -----------------------------------------------------------------------------

app = Flask(__name__)

# Configure SQLite database path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "workout_tracker.db")
app.config.update(
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_PATH}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize SQLAlchemy with this app
db.init_app(app)


# -----------------------------------------------------------------------------
# Routes (ordered by typical user flow)
# -----------------------------------------------------------------------------

@app.route("/")
def home():
    """Render the landing page."""
    return render_template("home.html")


@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    """Display the weekly schedule or handle creation of new workouts."""

    # ---- Create new workout(s) ---------------------------------------------
    if request.method == "POST":
        name = request.form.get("name")
        date_str = request.form.get("date")
        repeat_weekly = bool(request.form.get("repeat_weekly"))
        repeat_weeks = int(request.form.get("repeat_weeks") or 1)

        if name and date_str:
            workout_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            day_of_week = workout_date.strftime("%A")

            if repeat_weekly:
                for i in range(repeat_weeks):
                    repeated_date = workout_date + timedelta(weeks=i)
                    db.session.add(
                        Workout(
                            name=name,
                            date=repeated_date,
                            day_of_week=repeated_date.strftime("%A"),
                            repeat_weekly=True,
                        )
                    )
            else:
                db.session.add(
                    Workout(
                        name=name,
                        date=workout_date,
                        day_of_week=day_of_week,
                        repeat_weekly=False,
                    )
                )

            db.session.commit()
            return redirect(url_for("schedule"))

    # ---- Show weekly schedule ---------------------------------------------
    week_offset = int(request.args.get("week_offset", 0))
    today = datetime.today().date()

    # Start week on Sunday
    start_of_week = today - timedelta(
        days=today.weekday() + 1 if today.weekday() < 6 else 0
    )
    start_of_week += timedelta(weeks=week_offset)
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    workouts = Workout.query.filter(Workout.date.in_(week_dates)).all()

    week_schedule = {date.strftime("%A"): [] for date in week_dates}
    for workout in workouts:
        week_schedule[workout.day_of_week].append(workout)

    return render_template(
        "schedule.html",
        week_schedule=week_schedule,
        start_of_week=start_of_week,
        end_of_week=week_dates[-1],
        week_offset=week_offset,
    )


@app.route("/view/<int:workout_id>")
def view_workout(workout_id: int):
    """Display a single workout and its associated exercises."""
    workout = Workout.query.get_or_404(workout_id)

    workout_exercises = (
        db.session.query(WorkoutExercise)
        .filter_by(workout_id=workout.id)
        .join(Exercise)
        .all()
    )
    print(f"📋 Found {len(workout_exercises)} exercises for Workout ID {workout.id}")

    all_exercises = Exercise.query.all()
    return render_template(
        "view_workout.html",
        workout=workout,
        workout_exercises=workout_exercises,
        all_exercises=all_exercises,
    )


@app.route("/view/<int:workout_id>/add_exercises", methods=["POST"])
def add_exercises_to_workout(workout_id: int):
    """Attach selected exercises to an existing workout."""
    workout = Workout.query.get_or_404(workout_id)
    selected_ids = request.form.get("exercise_ids")
    print("📨 Raw POST data (selected_exercises):", selected_ids)

    if selected_ids:
        try:
            exercise_ids = json.loads(selected_ids)
            print("✅ Parsed exercise_ids:", exercise_ids)

            for ex_id in exercise_ids:
                print(f"🔄 Adding Exercise ID {ex_id} to Workout ID {workout.id}")
                db.session.add(
                    WorkoutExercise(workout_id=workout.id, exercise_id=int(ex_id))
                )

            db.session.commit()
            print("💾 Commit successful")
        except Exception as err:
            db.session.rollback()
            print("❌ Error saving exercises:", err)

    return redirect(url_for("view_workout", workout_id=workout.id))


@app.route("/view/<int:workout_id>/update_sets", methods=["POST"])
def update_sets(workout_id: int):
    """Update set number, reps, and weight for each WorkoutExercise entry."""
    Workout.query.get_or_404(workout_id)  # Ensure workout exists

    workout_exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).all()
    for we in workout_exercises:
        try:
            set_key = f"set_number_{we.id}"
            reps_key = f"reps_{we.id}"
            weight_key = f"weight_used_{we.id}"

            if set_key in request.form:
                we.set_number = (
                    int(request.form[set_key]) if request.form[set_key] else None
                )
            if reps_key in request.form:
                we.reps = (
                    int(request.form[reps_key]) if request.form[reps_key] else None
                )
            if weight_key in request.form:
                we.weight_used = (
                    float(request.form[weight_key]) if request.form[weight_key] else None
                )
        except Exception as err:
            print(f"❌ Error updating WorkoutExercise ID {we.id}: {err}")

    db.session.commit()
    print(f"✅ Updated sets/reps/weights for Workout {workout_id}")
    return redirect(url_for("view_workout", workout_id=workout_id))


@app.route("/view/<int:workout_id>/delete_exercise/<int:we_id>", methods=["POST"])
def delete_workout_exercise(workout_id: int, we_id: int):
    """Remove a specific exercise from a workout."""
    we = WorkoutExercise.query.get_or_404(we_id)
    if we.workout_id != workout_id:
        abort(404)

    db.session.delete(we)
    db.session.commit()
    return redirect(url_for("view_workout", workout_id=workout_id))


@app.route("/exercises")
def view_exercises():
    """List all exercises."""
    exercises = Exercise.query.all()
    return render_template("exercises.html", exercises=exercises)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Ensure tables exist before running the dev server
    with app.app_context():
        db.create_all()

    app.run(debug=True)
