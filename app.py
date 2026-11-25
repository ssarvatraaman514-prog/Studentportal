from flask import Flask, render_template_string, request, redirect
import sqlite3
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('students.db')
    conn.execute('CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, course TEXT, marks INTEGER)')
    return conn

STYLE = """
<style>
body{font-family:Arial;background:#f0f2f5;margin:0;padding:15px}
.box{max-width:600px;margin:auto;background:white;padding:20px;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.1)}
h1{text-align:center;color:#1a73e8}
input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:10px;font-size:16px;box-sizing:border-box}
button{width:100%;padding:13px;background:#1a73e8;color:white;border:none;border-radius:10px;font-size:17px;font-weight:bold}
table{width:100%;border-collapse:collapse;margin-top:15px}
th{background:#1a73e8;color:white;padding:10px}
td{padding:10px;border-bottom:1px solid #eee;text-align:center}
.del{color:red;text-decoration:none;font-weight:bold}
.link{display:block;text-align:center;margin-top:15px;color:#1a73e8}
</style>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = get_db()
    if request.method == 'POST':
        conn.execute('INSERT INTO students (name, course, marks) VALUES (?, ?, ?)', (request.form['name'], request.form['course'], request.form['marks']))
        conn.commit()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string(STYLE + '''
    <div class="box"><h1>📚 Students Portal</h1><p style="text-align:center">Admin - Wife Only</p>
    <form method="POST">
      <input name="name" placeholder="Student Ka Naam" required>
      <input name="course" placeholder="Class / Course" required>
      <input name="marks" placeholder="Marks" required>
      <button>➕ Add Student</button>
    </form>
    <table><tr><th>Name</th><th>Class</th><th>Marks</th><th>❌</th></tr>
    {% for s in students %}<tr><td>{{s[1]}}</td><td>{{s[2]}}</td><td>{{s[3]}}</td><td><a class="del" href="/delete/{{s[0]}}">Delete</a></td></tr>{% endfor %}
    </table>
    <a class="link" href="/teachers">👉 Teachers View Dekhne Ke Liye Yahan Click Karein</a>
    </div>
    ''', students=students)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit(); conn.close()
    return redirect('/')

@app.route('/teachers')
def teachers():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string(STYLE + '''
    <div class="box"><h1>📚 Class List</h1><p style="text-align:center">Sirf Dekhne Ke Liye</p>
    <table><tr><th>Name</th><th>Class</th><th>Marks</th></tr>
    {% for s in students %}<tr><td>{{s[1]}}</td><td>{{s[2]}}</td><td>{{s[3]}}</td></tr>{% endfor %}
    </table></div>
    ''', students=students)

if __name__ == '__main__':
    app.run()