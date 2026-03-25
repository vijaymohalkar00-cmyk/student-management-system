from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

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

# ---------- HOME ----------
@app.route('/')
def index():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template("index.html", students=students)

# ---------- ADD ----------
@app.route('/add', methods=['POST'])
def add():
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# ---------- EDIT ----------
@app.route('/edit/<int:id>')
def edit(id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template("edit.html", student=student)

# ---------- UPDATE ----------
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
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

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
