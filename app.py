from flask import Flask, render_template_string, abort, request, redirect, url_for
import re

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

members = []
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

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
<p><a href="/signup">Sign up as a member</a> | <a href="/members">View members ({{ member_count }})</a></p>
"""

PROGRAM_PAGE = """
<h1>{{ program.name }}</h1>
<h3>Weekly Workout Chart</h3>
<pre>{{ program.workout }}</pre>
<h3>Daily Nutrition Plan</h3>
<pre>{{ program.diet }}</pre>
<a href="/">Back</a>
"""

SIGNUP_PAGE = """
<h1>Member Signup</h1>
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
<form method="POST">
  Name: <input type="text" name="name"><br><br>
  Email: <input type="text" name="email"><br><br>
  <input type="submit" value="Sign Up">
</form>
<a href="/">Back</a>
"""

MEMBERS_PAGE = """
<h1>Members ({{ members|length }})</h1>
<ul>
{% for m in members %}
  <li>{{ m.name }} - {{ m.email }}</li>
{% endfor %}
</ul>
<a href="/">Back</a>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE, programs=programs, member_count=len(members))

@app.route('/program/<key>')
def program(key):
    p = programs.get(key)
    if not p:
        abort(404)
    return render_template_string(PROGRAM_PAGE, program=p)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()

        if not name:
            return render_template_string(SIGNUP_PAGE, error="Name cannot be empty.")
        if not EMAIL_REGEX.match(email):
            return render_template_string(SIGNUP_PAGE, error="Please enter a valid email address.")

        members.append({"name": name, "email": email})
        return redirect(url_for('members_list'))
    return render_template_string(SIGNUP_PAGE, error=None)

@app.route('/members')
def members_list():
    return render_template_string(MEMBERS_PAGE, members=members)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
