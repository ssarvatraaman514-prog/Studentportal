from flask import Flask, render_template_string, request, redirect
import sqlite3
app = Flask(__name__)
def get_db():
    conn = sqlite3.connect('students.db')
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, course TEXT, marks INTEGER)')
    return conn
@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db()
    if request.method == 'POST':
        conn.execute('INSERT INTO students (name, course, marks) VALUES (?, ?, ?)', (request.form['name'], request.form['course'], request.form['marks']))
        conn.commit()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string('''
    <h1>Students Portal - Admin</h1>
    <form method="POST">
      <input name="name" placeholder="Name" required>
      <input name="course" placeholder="Course" required>
      <input name="marks" placeholder="Marks" required>
      <button>Add Student</button>
    </form><hr>
    <table border="1"><tr><th>ID</th><th>Name</th><th>Course</th><th>Marks</th></tr>
    {% for s in students %}<tr><td>{{s[0]}}</td><td>{{s[1]}}</td><td>{{s[2]}}</td><td>{{s[3]}}</td></tr>{% endfor %}
    </table><br><a href="/teachers">Teachers View Link</a>
    ''', students=students)
@app.route('/teachers')
def teachers():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string('''
    <h1>Students Portal - Class List</h1>
    <p>Sirf dekhne ke liye hai.</p>
    <table border="1"><tr><th>ID</th><th>Name</th><th>Course</th><th>Marks</th></tr>
    {% for s in students %}<tr><td>{{s[0]}}</td><td>{{s[1]}}</td><td>{{s[2]}}</td><td>{{s[3]}}</td></tr>{% endfor %}
    </table>
    ''', students=students)
if __name__ == '__main__':
    app.run()
