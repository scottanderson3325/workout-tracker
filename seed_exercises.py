# seed_exercises.py

from app import app, db
from models import Exercise

def seed_exercises():
    exercises = [
        Exercise(
            name="Push-Up",
            instructions="Start in a high plank position with your hands under your shoulders. Lower your body until your chest almost touches the floor, then push back up.",
            video_url="https://youtu.be/IODxDxX7oi4",
            primary_muscle="Chest",
            secondary_muscles="Triceps, Shoulders",
            stabilizers="Core"
        ),
        Exercise(
            name="Barbell Front Squat",
            instructions="Rest the barbell on your front delts with elbows high. Squat down keeping your chest up and knees out.",
            video_url="https://youtu.be/tlfGU9SL0jM",
            primary_muscle="Quads",
            secondary_muscles="Glutes, Hamstrings",
            stabilizers="Core, Erectors"
        ),
        Exercise(
            name="Dumbbell Lunges",
            instructions="Step forward with one leg and lower your body until both knees are at 90-degree angles. Push back to standing.",
            video_url="https://youtu.be/QF0BQS2W80k",
            primary_muscle="Quads",
            secondary_muscles="Glutes, Hamstrings",
            stabilizers="Core"
        ),
        Exercise(
            name="Dumbbell Bench",
            instructions="Lie on a bench holding dumbbells at chest level. Press upward until arms are extended, then lower slowly.",
            video_url="https://youtu.be/1oed-UmAxFs",
            primary_muscle="Chest",
            secondary_muscles="Triceps, Shoulders",
            stabilizers="Core"
        ),
        Exercise(
            name="Barbell Row",
            instructions="Bend at the hips, keep a flat back, and row the barbell to your lower rib cage.",
            video_url="https://youtu.be/vT2GjY_Umpw",
            primary_muscle="Lats",
            secondary_muscles="Rear Delts, Biceps",
            stabilizers="Core, Hamstrings"
        ),
        Exercise(
            name="Weighted Pull-Up",
            instructions="Use a belt or hold a dumbbell between your legs. Perform a pull-up with full range of motion.",
            video_url="https://youtu.be/VL5Ab0T07e4",
            primary_muscle="Lats",
            secondary_muscles="Biceps, Rear Delts",
            stabilizers="Core"
        ),
        Exercise(
            name="Barbell Deadlift",
            instructions="Stand with feet hip-width, grip the bar just outside your knees, and lift by extending your hips and knees simultaneously.",
            video_url="https://youtu.be/op9kVnSso6Q",
            primary_muscle="Glutes",
            secondary_muscles="Hamstrings, Quads",
            stabilizers="Core, Erectors, Lats"
        ),
        Exercise(
            name="Barbell RDL",
            instructions="Keep your legs slightly bent, hinge at the hips, and lower the bar while keeping your back flat. Return to standing.",
            video_url="https://youtu.be/0zG3WrU3KCE",
            primary_muscle="Hamstrings",
            secondary_muscles="Glutes",
            stabilizers="Core, Erectors"
        ),
    ]

    db.session.bulk_save_objects(exercises)
    db.session.commit()
    print(f"✅ Seeded {len(exercises)} exercises successfully.")

if __name__ == "__main__":
    with app.app_context():
        seed_exercises()
