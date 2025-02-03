import sqlite3
from flask import Flask, redirect, render_template, request, jsonify, g

app = Flask(__name__)
DATABASE = 'Calender.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/announcements')
def get_announcements():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM announcements ORDER BY announcement_date")
    announcements = cursor.fetchall()
    announcements_list = []
    for ann in announcements:
        announcements_list.append({
            'id': ann[0],
            'professor_name': ann[1],
            'title': ann[2],
            'description': ann[3],
            'announcement_date': ann[4],
            'created_at': ann[5]
        })
    return jsonify(announcements_list)

@app.route('/')  # Route for the main page (calendar)
def index():
    return render_template('index.html')  # Render the index.html template 


@app.route('/add_announcement', methods=['GET', 'POST'])  # New route
def add_announcement():
    if request.method == 'POST':
        professor_name = request.form['professor_name']
        title = request.form['title']
        description = request.form['description']
        announcement_date = request.form['announcement_date']

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO announcements (professor_name, title, description, announcement_date) VALUES (?, ?, ?, ?)", (professor_name, title, description, announcement_date))
            db.commit()
            return redirect("/")  # Redirect back to the calendar page
        except Exception as e:
            return f"Error inserting data: {str(e)}"  # Handle errors (improve this later)

    return render_template('add_announcement.html')  # Render the form page (GET request)

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode