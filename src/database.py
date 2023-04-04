import sqlite3
import os
from werkzeug.security import check_password_hash, generate_password_hash


try:
    os.remove("school.db")
except:
    pass


db = sqlite3.connect("school.db")
db.isolation_level = None


db.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, visible BOOLEAN)")
db.execute("CREATE TABLE Admins (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES Users)")
db.execute("CREATE TABLE Teachers (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES Users)")
db.execute("CREATE TABLE Students (id INTEGER PRIMARY KEY, name TEXT, credits INTEGER, user_id INTEGER REFERENCES Users)")
db.execute("CREATE TABLE Courses (id INTEGER PRIMARY KEY, name TEXT, credits INTEGER)")
db.execute("CREATE TABLE CoursesTeachers (course_id INTEGER REFERENCES Courses, teacher_id INTEGER REFERENCES Teachers)")
db.execute("CREATE TABLE CoursesStudents (course_id INTEGER REFERENCES Courses, student_id INTEGER REFERENCES Students)")
db.execute("CREATE TABLE Credits (id INTEGER PRIMARY KEY, student_id INTEGER REFERENCES Students, course_id INTEGER REFERENCES Courses, date DATE, grade INTEGER)")
db.execute("CREATE TABLE StudentsCredits (student_id INTEGER REFERENCES Students, course_id INTEGER REFERENCES Courses)")


def create_admin(name:str, username: str, password: str):
    password_hash = generate_password_hash(password)
    user_id = db.execute("INSERT INTO Users (username, password, visible) VALUES (?, ?, ?)", [username, password_hash, 1]).lastrowid
    db.execute("INSERT INTO Admins (name, user_id) VALUES (?, ?)", [name, user_id])
    return True

def create_teacher(name: str, username: str, password: str):
    password_hash = generate_password_hash(password)
    user_id = db.execute("INSERT INTO Users (username, password, visible) VALUES (?, ?, ?)", [username, password_hash, 1]).lastrowid
    db.execute("INSERT INTO Teachers (name, user_id) VALUES (?, ?)", [name, user_id])
    return True

def create_student(name: str, username: str, password: str):
    password_hash = generate_password_hash(password)
    user_id = db.execute("INSERT INTO Users (username, password, visible) VALUES (?, ?, ?)", [username, password_hash, 1]).lastrowid
    db.execute("INSERT INTO Students (name, user_id) VALUES (?, ?)", [name, user_id])
    data = db.execute("SELECT * FROM users").fetchall()
    return True

def delete_teacher(teacher_username: str):
    db.execute("UPDATE users SET visible=0 WHERE username=?", [teacher_username])
    return True

def get_password(username):
    password = db.execute("SELECT password FROM users WHERE visible=1 AND LOWER(username)=?", [username.lower()]).fetchone()
    if password != None:
        return password[0]
    return None
