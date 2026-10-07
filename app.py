from flask import Flask, render_template_string, abort

app = Flask(__name__)

programs = {
    "fat-loss": {
        "name": "Fat Loss (FL)",
        "workout": "Mon: 5x5 Back Squat + AMRAP\nTue: EMOM 20min Assault Bike\nWed: Bench Press + 21-15-9\nThu: 10RFT Deadlifts/Box Jumps\nFri: 30min Active Recovery",
        "diet": "B: 3 Egg Whites + Oats Idli\nL: Grilled Chicken + Brown Rice\nD: Fish Curry + Millet Roti\nTarget: 2,000 kcal"
    },
    "muscle-gain": {
        "name": "Muscle Gain (MG)",
        "workout": "Mon: Squat 5x5\nTue: Bench 5x5\nWed: Deadlift 4x6\nThu: Front Squat 4x8\nFri: Incline Press 4x10\nSat: Barbell Rows 4x10",
        "diet": "B: 4 Eggs + PB Oats\nL: Chicken Biryani (250g Chicken)\nD: Mutton Curry + Jeera Rice\nTarget: 3,200 kcal"
    },
    "beginner": {
        "name": "Beginner (BG)",
        "workout": "Circuit Training: Air Squats, Ring Rows, Push-ups.\nFocus: Technique Mastery & Form",
        "diet": "Balanced Meals: Idli-Sambar, Rice-Dal, Chapati.\nProtein: 120g/day"
    }
}

HOME_PAGE = """
<h1>ACEest Fitness and Gym</h1>
<p>Select a program:</p>
<ul>
{% for key, p in programs.items() %}
  <li><a href="/program/{{ key }}">{{ p.name }}</a></li>
{% endfor %}
</ul>
<hr>
<p>Capacity: 150 Users | Area: 10,000 sq ft | Break-even: 250 Members</p>
"""

PROGRAM_PAGE = """
<h1>{{ program.name }}</h1>
<h3>Weekly Workout Chart</h3>
<pre>{{ program.workout }}</pre>
<h3>Daily Nutrition Plan</h3>
<pre>{{ program.diet }}</pre>
<a href="/">Back</a>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE, programs=programs)

@app.route('/program/<key>')
def program(key):
    p = programs.get(key)
    if not p:
        abort(404)
    return render_template_string(PROGRAM_PAGE, program=p)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
