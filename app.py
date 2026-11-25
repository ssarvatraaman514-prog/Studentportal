from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS student_list
    (id INTEGER PRIMARY KEY, name TEXT, course TEXT, marks INTEGER)''')
    return conn

@app.route('/')
def home():
    conn = get_db()
    data = conn.execute("SELECT * FROM student_list").fetchall()
    conn.close()
    html = """
    <h2>Student Management System</h2>
    <form method="post" action="/add">
    ID: <input name="id"><br><br>
    Name: <input name="name"><br><br>
    Course: <input name="course"><br><br>
    Marks: <input name="marks"><br><br>
    <button>Add Student</button>
    </form><hr>
    <table border="1"><tr><th>ID</th><th>Name</th><th>Course</th><th>Marks</th></tr>
    {% for r in data %}
    <tr><td>{{r[0]}}</td><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td></tr>
    {% endfor %}</table>
    """
    return render_template_string(html, data=data)

@app.route('/add', methods=['POST'])
def add():
    conn = get_db()
    conn.execute("INSERT INTO student_list VALUES (?,?,?,?)",
    (request.form['id'], request.form['name'], request.form['course'], request.form['marks']))
    conn.commit()
    conn.close()
    return '<h3>Added Successfully!</h3><a href="/">Back</a>'

if __name__ == '__main__':
    app.run()
