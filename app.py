from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DATABASE ----------
def connect():
    return sqlite3.connect("students.db")

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        department TEXT
    )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid Credentials"

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ---------- HOME + DASHBOARD ----------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    conn = connect()
    cursor = conn.cursor()

    # all students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # total count
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    # department wise count
    cursor.execute("SELECT department, COUNT(*) FROM students GROUP BY department")
    dept_data = cursor.fetchall()

    conn.close()

    return render_template("index.html", students=students, total=total, dept_data=dept_data)

# ---------- ADD ----------
@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    name = request.form['name']
    age = request.form['age']
    dept = request.form['department']

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, age, department) VALUES (?, ?, ?)",
        (name, age, dept)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- DELETE ----------
@app.route('/delete/<int:id>')
def delete(id):
    if 'user' not in session:
        return redirect('/login')

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- EDIT ----------
@app.route('/edit/<int:id>')
def edit(id):
    if 'user' not in session:
        return redirect('/login')

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template("edit.html", student=student)

# ---------- UPDATE ----------
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user' not in session:
        return redirect('/login')

    name = request.form['name']
    age = request.form['age']
    dept = request.form['department']

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students 
        SET name=?, age=?, department=? 
        WHERE id=?
    """, (name, age, dept, id))

    conn.commit()
    conn.close()

    return redirect('/')

# ---------- SEARCH ----------
@app.route('/search', methods=['POST'])
def search():
    if 'user' not in session:
        return redirect('/login')

    keyword = request.form['keyword']

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + keyword + '%',))
    students = cursor.fetchall()
    conn.close()

    return render_template("index.html", students=students, total=len(students), dept_data=[])

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
