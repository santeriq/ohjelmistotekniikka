import sqlite3
import os
from werkzeug.security import check_password_hash, generate_password_hash



# creating database and deleting it
db = sqlite3.connect("school.db")
db.isolation_level = None

try:
    db.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, visible BOOLEAN)")
    db.execute("CREATE TABLE Courses (id INTEGER PRIMARY KEY, tag TEXT, name TEXT, credits INTEGER, open BOOLEAN, visible BOOLEAN)")
    db.execute("CREATE TABLE StudentRoleRequests (id INTEGER PRIMARY KEY, username TEXT, message TEXT, datetime DATETIME)")
except sqlite3.OperationalError:
    pass

db.commit()
db.close()


def delete_database():
    try:
        os.remove("school.db")
        return True
    except Exception as error:
        return error


# database main functions
def create_user(username: str, password: str):
    password_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("INSERT INTO Users (username, password, role, visible) VALUES (?, ?, ?, ?)", [username, password_hash, "none", 1])
    db.commit()
    db.close()
    return f"created new user: {username}"

def create_admin(username:str, password: str):
    password_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("INSERT INTO Users (username, password, role, visible) VALUES (?, ?, ?, ?)", [username, password_hash, "admin", 1])
    db.commit()
    db.close()
    return f"created new admin: {username}"

def create_teacher(username: str, password: str):
    password_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("INSERT INTO Users (username, password, role, visible) VALUES (?, ?, ?, ?)", [username, password_hash, "teacher", 1])
    db.commit()
    db.close()
    return f"created new teacher: {username}"

def create_student(username: str, password: str):
    password_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("INSERT INTO Users (username, password, role, visible) VALUES (?, ?, ?, ?)", [username, password_hash, "student", 1])
    db.commit()
    db.close()
    return f"created new student: {username}"

def create_course(tag, name, credits):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("INSERT INTO Courses (tag, name, credits, open, visible) VALUES (?, ?, ?, ?, ?)", [tag, name, credits, 1, 1])
    db.commit()
    db.close()
    return f"created new course: {name} / {credits} / {tag}"

def close_course(tag):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE courses SET open=0 WHERE tag=?", [tag])
    db.commit()
    db.close()
    return True

def open_course(tag):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE courses SET open=1 WHERE tag=?", [tag])
    db.commit()
    db.close()
    return True

def delete_teacher(teacher_username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE users SET visible=0 WHERE username=?", [teacher_username])
    db.commit()
    db.close()
    return True

def get_password(username):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    password = db.execute("SELECT password FROM users WHERE visible=1 AND LOWER(username)=?", [username.lower()]).fetchone()
    db.commit()
    db.close()
    if password != None:
        return password[0]
    return None

def search_username(username):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    found = db.execute("SELECT username FROM users WHERE visible=1 AND LOWER(username)=?", [username.lower()]).fetchall()
    db.commit()
    db.close()
    return found

def get_user_role(username):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    role = db.execute("SELECT role FROM users WHERE LOWER(username)=?", [username.lower()]).fetchall()
    db.commit()
    db.close()
    role = role[0][0]
    return role

def set_user_role(username, role):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE users SET role=? WHERE username=?", [role, username])
    db.commit()
    db.close()
    return f'set "{username}" as {role}'

def get_courses_list_sorted_by_name():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    list = db.execute("SELECT * FROM courses WHERE visible=1 ORDER BY name").fetchall()
    db.commit()
    db.close()
    return list

def get_courses_list_sorted_by_credits():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    list = db.execute("SELECT * FROM courses WHERE visible=1 ORDER BY credits DESC").fetchall()
    db.commit()
    db.close()
    return list

def get_courses_list_sorted_by_tag():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    list = db.execute("SELECT * FROM courses WHERE visible=1 ORDER BY tag").fetchall()
    db.commit()
    db.close()
    return list

def get_courses_list_sorted_by_status():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    list = db.execute("SELECT * FROM courses WHERE visible=1 ORDER BY open DESC").fetchall()
    db.commit()
    db.close()
    return list

def search_course_tag(tag):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("SELECT tag FROM courses WHERE visible=1 AND tag=?", [tag]).fetchall()
    db.commit()
    db.close()
    return data

def new_studentrole_request(username, message, datetime):
    if message == "":
        message = "-"
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("INSERT INTO StudentRoleRequests (username, message, datetime) VALUES (?, ?, ?)", [username, message, datetime])
    db.commit()
    db.close()
    return f"New student role request created: {username} / {message} / {datetime}"

def update_studentrole_request(username, message, datetime):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE StudentRoleRequests SET message=? WHERE username=?", [message, username])
    db.execute("UPDATE StudentRoleRequests SET datetime=? WHERE username=?", [datetime, username])
    db.commit()
    db.close()
    return f"Updated student role request: {username} / {message} / {datetime}"

def get_studentrole_requests_list():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    list = db.execute("SELECT * FROM StudentRoleRequests ORDER BY id").fetchall()
    db.commit()
    db.close()
    return list

def get_studentrole_requests_list_sorted_by_username():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    list = db.execute("SELECT * FROM StudentRoleRequests ORDER BY username").fetchall()
    db.commit()
    db.close()
    return list

def get_studentrole_request_of_user(username):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    request = db.execute("SELECT * FROM StudentRoleRequests WHERE username=?", [username]).fetchall()
    db.commit()
    db.close()
    return request

def accept_studentrole_request(username):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("DELETE FROM StudentRoleRequests WHERE username=?", [username])
    db.commit()
    db.close()
    set_user_role(username, "student")
    return f"Accepted student role request from {username}"

def reject_studentrole_request(username):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("DELETE FROM StudentRoleRequests WHERE username=?", [username])
    db.commit()
    db.close()
    return f"Delete student role request from {username}"

