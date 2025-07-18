from flask import Flask, render_template, request

app = Flask(__name__)

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
        return render_template("schedule.html", workouts=workouts)

    return render_template("schedule.html", workouts={})

if __name__ == '__main__':
    app.run(debug=True)
