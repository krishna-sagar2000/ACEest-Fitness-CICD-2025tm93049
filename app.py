from flask import Flask, render_template_string, abort, request, redirect, url_for
import re
import logging
from collections import Counter

app = Flask(__name__)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
bookings = []
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TIME_SLOTS = ["7:00 AM", "9:00 AM", "5:00 PM", "7:00 PM"]

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
<p>
  <a href="/signup">Sign up as a member</a> | 
  <a href="/members">View members ({{ member_count }})</a> | 
  <a href="/book">Book a trainer session</a> | 
  <a href="/bookings">View bookings ({{ booking_count }})</a> | 
  <a href="/analytics">View analytics</a>
</p>
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

BOOK_PAGE = """
<h1>Book a Trainer Session</h1>
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
<form method="POST">
  Name: <input type="text" name="name"><br><br>
  Program:
  <select name="program">
    {% for key, p in programs.items() %}
      <option value="{{ key }}">{{ p.name }}</option>
    {% endfor %}
  </select><br><br>
  Time Slot:
  <select name="slot">
    {% for slot in slots %}
      <option value="{{ slot }}">{{ slot }}</option>
    {% endfor %}
  </select><br><br>
  <input type="submit" value="Book Session">
</form>
<a href="/">Back</a>
"""

BOOKINGS_PAGE = """
<h1>Bookings ({{ bookings|length }})</h1>
<ul>
{% for b in bookings %}
  <li>{{ b.name }} - {{ b.program }} - {{ b.slot }}</li>
{% endfor %}
</ul>
<a href="/">Back</a>
"""

ANALYTICS_PAGE = """
<h1>Analytics</h1>
<p>Total Members: {{ total_members }}</p>
<p>Total Bookings: {{ total_bookings }}</p>
<p>Most Booked Program: {{ top_program }}</p>
<h3>Bookings per Program</h3>
<ul>
{% for prog, count in program_counts %}
  <li>{{ prog }}: {{ count }}</li>
{% endfor %}
</ul>
<a href="/">Back</a>
"""

ERROR_404_PAGE = """
<h1 style="color:#c0392b;">404 - Page Not Found</h1>
<p>Sorry, the page or program you're looking for doesn't exist.</p>
<a href="/">Go back home</a>
"""

ERROR_500_PAGE = """
<h1 style="color:#c0392b;">500 - Internal Server Error</h1>
<p>Something went wrong on our end. Please try again later.</p>
<a href="/">Go back home</a>
"""

@app.errorhandler(404)
def not_found_error(error):
    logging.warning(f"404 error: {request.path}")
    return render_template_string(ERROR_404_PAGE), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 error: {request.path}")
    return render_template_string(ERROR_500_PAGE), 500

@app.route('/')
def home():
    logging.info("Home page visited")
    return render_template_string(HOME_PAGE, programs=programs, member_count=len(members), booking_count=len(bookings))

@app.route('/program/<key>')
def program(key):
    p = programs.get(key)
    if not p:
        logging.warning(f"Invalid program requested: {key}")
        abort(404)
    logging.info(f"Program viewed: {key}")
    return render_template_string(PROGRAM_PAGE, program=p)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name:
            logging.warning("Signup failed: empty name")
            return render_template_string(SIGNUP_PAGE, error="Name cannot be empty.")
        if not EMAIL_REGEX.match(email):
            logging.warning(f"Signup failed: invalid email '{email}'")
            return render_template_string(SIGNUP_PAGE, error="Please enter a valid email address.")
        members.append({"name": name, "email": email})
        logging.info(f"New member signed up: {name} ({email})")
        return redirect(url_for('members_list'))
    return render_template_string(SIGNUP_PAGE, error=None)

@app.route('/members')
def members_list():
    return render_template_string(MEMBERS_PAGE, members=members)

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        program_key = request.form.get('program')
        slot = request.form.get('slot')
        if not name:
            logging.warning("Booking failed: empty name")
            return render_template_string(BOOK_PAGE, error="Name cannot be empty.", programs=programs, slots=TIME_SLOTS)
        bookings.append({"name": name, "program": programs[program_key]["name"], "slot": slot})
        logging.info(f"New booking: {name} - {programs[program_key]['name']} - {slot}")
        return redirect(url_for('bookings_list'))
    return render_template_string(BOOK_PAGE, error=None, programs=programs, slots=TIME_SLOTS)

@app.route('/bookings')
def bookings_list():
    return render_template_string(BOOKINGS_PAGE, bookings=bookings)

@app.route('/analytics')
def analytics():
    program_names = [b['program'] for b in bookings]
    counts = Counter(program_names)
    top_program = counts.most_common(1)[0][0] if counts else "No bookings yet"
    return render_template_string(
        ANALYTICS_PAGE,
        total_members=len(members),
        total_bookings=len(bookings),
        top_program=top_program,
        program_counts=counts.most_common()
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
