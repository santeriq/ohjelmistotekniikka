import sqlite3
import os
from werkzeug.security import generate_password_hash


# creating database and deleting it
database = sqlite3.connect("school.db")
database.isolation_level = None

try:
    database.execute("""
                CREATE TABLE Users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                role INTEGER,
                visible BOOLEAN
                )""")
    database.execute("""
                CREATE TABLE Courses (
                id INTEGER PRIMARY KEY, 
                tag TEXT, 
                name TEXT, 
                credits INTEGER, 
                open BOOLEAN, 
                visible BOOLEAN
                )""")
    database.execute("""
                CREATE TABLE StudentRoleRequests (
                id INTEGER PRIMARY KEY, 
                username TEXT, 
                message TEXT, 
                datetime DATETIME
                )""")
except sqlite3.OperationalError:
    pass

database.commit()
database.close()


def delete_database():
    try:
        os.remove("school.db")
        return True
    except FileNotFoundError as error:
        return error


# database main functions
def create_user(username: str, password: str):
    password_hash = generate_password_hash(password)
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
                """,
                              [username, password_hash, 3, 1])
    function_database.commit()
    function_database.close()
    return f"created new user: {username}"


def create_admin(username: str, password: str):
    password_hash = generate_password_hash(password)
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
                """,
                              [username, password_hash, 0, 1])
    function_database.commit()
    function_database.close()
    return f"created new admin: {username}"


def create_teacher(username: str, password: str):
    password_hash = generate_password_hash(password)
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
                """,
                              [username, password_hash, 1, 1])
    function_database.commit()
    function_database.close()
    return f"created new teacher: {username}"


def create_student(username: str, password: str):
    password_hash = generate_password_hash(password)
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
                """,
                              [username, password_hash, 2, 1])
    function_database.commit()
    function_database.close()
    return f"created new student: {username}"


def create_course(tag, name, credits_input):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                INSERT INTO Courses
                (tag, name, credits, open, visible)
                VALUES
                (?, ?, ?, ?, ?)
                """,
                              [tag, name, credits_input, 1, 1]
                              )
    function_database.commit()
    function_database.close()
    return f"created new course: {name} / {credits_input} / {tag}"


def close_course(tag):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("UPDATE courses SET open=0 WHERE tag=?", [tag])
    function_database.commit()
    function_database.close()
    return True


def open_course(tag):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("UPDATE courses SET open=1 WHERE tag=?", [tag])
    function_database.commit()
    function_database.close()
    return True


def delete_teacher(teacher_username: str):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute(
        "UPDATE users SET visible=0 WHERE username=?", [teacher_username])
    function_database.commit()
    function_database.close()
    return True


def get_password(username):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    password = function_database.execute("""
                            SELECT password
                            FROM users
                            WHERE visible=1
                            AND LOWER(username)=?
                            """,
                                         [username.lower()]).fetchone()
    function_database.commit()
    function_database.close()
    if password is not None:
        return password[0]
    return None


def search_username(username):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    found = function_database.execute("""
                       SELECT username
                       FROM users
                       WHERE visible=1
                       AND LOWER(username)=?
                       """,
                                      [username.lower()]).fetchall()
    function_database.commit()
    function_database.close()
    return found


def get_user_role(username):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    role = function_database.execute("""
                      SELECT role
                      FROM users
                      WHERE LOWER(username)=?
                      """,
                                     [username.lower()]).fetchall()
    function_database.commit()
    function_database.close()
    role = role[0][0]
    return role


def set_user_role(username, role):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("UPDATE users SET role=? WHERE username=?", [role, username])
    function_database.commit()
    function_database.close()
    return f'set "{username}" as {role}'


def get_courses_list_sorted_by_name():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    courses_list = function_database.execute("""
                                        SELECT * 
                                        FROM courses 
                                        WHERE visible=1 
                                        ORDER BY name
                                    """
                                             ).fetchall()
    function_database.commit()
    function_database.close()
    return courses_list


def get_courses_list_sorted_by_credits():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    courses_list = function_database.execute("""
                                        SELECT *
                                        FROM courses
                                        WHERE visible=1
                                        ORDER BY credits DESC
                                    """
                                             ).fetchall()
    function_database.commit()
    function_database.close()
    return courses_list


def get_courses_list_sorted_by_tag():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    courses_list = function_database.execute("""
                                        SELECT *
                                        FROM courses
                                        WHERE visible=1
                                        ORDER BY tag
                                        """
                                             ).fetchall()
    function_database.commit()
    function_database.close()
    return courses_list


def get_courses_list_sorted_by_status():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    courses_list = function_database.execute("""
                                        SELECT *
                                        FROM courses
                                        WHERE visible=1
                                        ORDER BY open DESC
                                        """
                                             ).fetchall()
    function_database.commit()
    function_database.close()
    return courses_list


def search_course_tag(tag):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT tag
                                        FROM courses
                                        WHERE visible=1
                                        AND tag=?
                                    """,
                                     [tag]).fetchall()
    function_database.commit()
    function_database.close()
    return data


def new_studentrole_request(username, message, datetime):
    if message == "":
        message = "-"
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                INSERT INTO StudentRoleRequests
                (username, message, datetime)
                VALUES
                (?, ?, ?)
                """,
                              [username, message, datetime])
    function_database.commit()
    function_database.close()
    return f"New student role request created: {username} / {message} / {datetime}"


def update_studentrole_request(username, message, datetime):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute("""
                                UPDATE StudentRoleRequests
                                SET message=?
                                WHERE username=?
                            """,
                              [message, username])
    function_database.execute("""
                                UPDATE StudentRoleRequests
                                SET datetime=?
                                WHERE username=?
                            """,
                              [datetime, username])
    function_database.commit()
    function_database.close()
    return f"Updated student role request: {username} / {message} / {datetime}"


def get_studentrole_requests_list():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    requests = function_database.execute(
        "SELECT * FROM StudentRoleRequests ORDER BY id").fetchall()
    function_database.commit()
    function_database.close()
    return requests


def get_studentrole_requests_list_sorted_by_username():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    requests = function_database.execute("""
                                        SELECT *
                                        FROM StudentRoleRequests
                                        ORDER BY username
                                    """).fetchall()
    function_database.commit()
    function_database.close()
    return requests


def get_studentrole_request_of_user(username):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    request = function_database.execute("""
                         SELECT *
                         FROM StudentRoleRequests
                         WHERE username=?
                         """,
                                        [username]).fetchall()
    function_database.commit()
    function_database.close()
    return request

def get_all_users_list():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE visible=1
                                    """).fetchall()
    function_database.close()
    return data

def get_all_users_list_sorted_by_name():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE visible=1
                                        ORDER BY username
                                    """).fetchall()
    function_database.close()
    return data

def get_all_users_list_sorted_by_role():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE visible=1
                                        ORDER BY role
                                    """).fetchall()
    function_database.close()
    return data

def get_all_students_list():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=2
                                        AND visible=1
                                    """).fetchall()
    function_database.close()
    return data

def get_all_students_list_sorted_by_name():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=2
                                        AND visible=1
                                        ORDER BY username
                                    """).fetchall()
    function_database.close()
    return data

def get_all_teachers_list():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=1
                                        AND visible=1
                                    """).fetchall()
    function_database.close()
    return data

def get_all_teachers_list_sorted_by_name():
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    data = function_database.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=1
                                        AND visible=1
                                        ORDER BY username
                                    """).fetchall()
    function_database.close()
    return data

def accept_studentrole_request(username):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute(
        "DELETE FROM StudentRoleRequests WHERE username=?", [username])
    function_database.commit()
    function_database.close()
    set_user_role(username, 2)
    return f"Accepted student role request from {username}"


def reject_studentrole_request(username):
    function_database = sqlite3.connect("school.db")
    function_database.isolation_level = None
    function_database.execute(
        "DELETE FROM StudentRoleRequests WHERE username=?", [username])
    function_database.commit()
    function_database.close()
    return f"Delete student role request from {username}"
