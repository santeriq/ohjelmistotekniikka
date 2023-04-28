import sqlite3
import os
from werkzeug.security import generate_password_hash


# creating database and deleting it

def create_database():
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
        database.execute("""
                            CREATE TABLE InCourse (
                            course_id INTEGER REFERENCES Courses,
                            course_tag TEXT REFERENCES Courses,
                            course_name TEXT REFERENCES Courses,
                            course_credits INTEGER REFERENCES Courses,
                            user_id INTEGER REFERENCES Users,
                            username TEXT REFERENCS Users,
                            user_role INTEGER REFERENCES Users,
                            grade INTEGER,
                            user_visible BOOLEAN
                    )""")
        database.commit()
        database.close()
        return "Created database school.db"
    except sqlite3.OperationalError as error:
        return error



def delete_database():
    try:
        os.remove("school.db")
        return True
    except FileNotFoundError as error:
        return error


# database main functions
def create_user(username: str, password: str):
    password_hash = generate_password_hash(password)
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                                INSERT INTO Users
                                (username, password, role, visible)
                                VALUES
                                (?, ?, ?, ?)
                            """,
                                [username, password_hash, 3, 1])
    func_db.commit()
    func_db.close()
    return f"created new user: {username}"


def create_admin(username: str, password: str):
    password_hash = generate_password_hash(password)
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                                INSERT INTO Users
                                (username, password, role, visible)
                                VALUES
                                (?, ?, ?, ?)
                            """,
                                [username, password_hash, 0, 1])
    func_db.commit()
    func_db.close()
    return f"created new admin: {username}"


def create_teacher(username: str, password: str):
    password_hash = generate_password_hash(password)
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                                INSERT INTO Users
                                (username, password, role, visible)
                                VALUES
                                (?, ?, ?, ?)
                            """,
                                [username, password_hash, 1, 1])
    func_db.commit()
    func_db.close()
    return f"created new teacher: {username}"


def create_student(username: str, password: str):
    password_hash = generate_password_hash(password)
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
                """,
                              [username, password_hash, 2, 1])
    func_db.commit()
    func_db.close()
    return f"created new student: {username}"


def create_course(tag, name, credits_input):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                INSERT INTO Courses
                (tag, name, credits, open, visible)
                VALUES
                (?, ?, ?, ?, ?)
                """,
                              [tag, name, credits_input, 1, 1]
                              )
    func_db.commit()
    func_db.close()
    return f"created new course: {name} / {credits_input} / {tag}"


def close_course(tag):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("UPDATE courses SET open=0 WHERE tag=?", [tag])
    func_db.commit()
    func_db.close()
    return True


def open_course(tag):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("UPDATE courses SET open=1 WHERE tag=?", [tag])
    func_db.commit()
    func_db.close()
    return True

def join_course(course_tag, username):
    course_info = get_course_info(course_tag)
    course_id = course_info[0]
    course_name = course_info[2]
    course_credits = course_info[3]
    user_info = get_user_info(username)
    user_id = user_info[0]
    user_role = user_info[3]
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                        INSERT INTO InCourse 
                        (course_id, course_tag, course_name, course_credits, user_id, username, user_role, grade, user_visible)
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    , [course_id, course_tag, course_name, course_credits, user_id, username, user_role, 0, 1])
    func_db.commit()
    func_db.close()
    return f"User {username} joined course {course_tag}"

def leave_course(course_tag: str, username: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                        DELETE FROM InCourse 
                        WHERE course_tag=?
                        AND username=?
                    """
                    , [course_tag, username])
    func_db.commit()
    func_db.close()
    return f'User "{username}" left course {course_tag}'


def delete_teacher(teacher_username: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute(
        "UPDATE users SET visible=0 WHERE username=?", [teacher_username])
    func_db.commit()
    func_db.close()
    return True

def get_course_info(tag: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("SELECT * FROM courses WHERE tag=? AND visible=1", [tag]).fetchone()
    func_db.close()
    return data

def get_users_in_course(tag: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("SELECT * FROM InCourse WHERE course_tag=? AND user_visible=1", [tag]).fetchall()
    func_db.close()
    return data

def get_students_in_course(tag: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("SELECT username, grade FROM InCourse WHERE course_tag=? AND user_role=2 AND user_visible=1 ORDER BY username", [tag]).fetchall()
    func_db.close()
    return data

def get_users_courses(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("SELECT * FROM InCourse WHERE username=? AND user_visible=1 ORDER BY course_name", [username]).fetchall()
    func_db.close()
    return data

def search_user_in_course(username: str, course_tag: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("SELECT * FROM InCourse WHERE username=? AND course_tag=? AND user_visible=1", [username, course_tag]).fetchall()
    func_db.close()
    return data

def get_user_info(username: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("SELECT * FROM users WHERE username=? AND visible=1", [username]).fetchone()
    func_db.close()
    return data

def get_password(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    password = func_db.execute("""
                            SELECT password
                            FROM users
                            WHERE visible=1
                            AND LOWER(username)=?
                            """,
                                         [username.lower()]).fetchone()
    func_db.commit()
    func_db.close()
    if password is not None:
        return password[0]
    return None


def search_username(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    found = func_db.execute("""
                       SELECT username
                       FROM users
                       WHERE visible=1
                       AND LOWER(username)=?
                       """,
                                      [username.lower()]).fetchall()
    func_db.commit()
    func_db.close()
    return found


def get_user_role(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    role = func_db.execute("""
                      SELECT role
                      FROM users
                      WHERE LOWER(username)=?
                      """,
                                     [username.lower()]).fetchall()
    func_db.commit()
    func_db.close()
    role = role[0][0]
    return role


def set_user_role(username, role):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("UPDATE users SET role=? WHERE username=?", [role, username])
    func_db.commit()
    func_db.close()
    return f'set "{username}" as {role}'


def get_courses_list_sorted_by_name():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    courses_list = func_db.execute("""
                                        SELECT * 
                                        FROM courses 
                                        WHERE visible=1 
                                        ORDER BY name
                                    """
                                             ).fetchall()
    func_db.commit()
    func_db.close()
    return courses_list


def get_courses_list_sorted_by_credits():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    courses_list = func_db.execute("""
                                        SELECT *
                                        FROM courses
                                        WHERE visible=1
                                        ORDER BY credits DESC
                                    """
                                             ).fetchall()
    func_db.commit()
    func_db.close()
    return courses_list


def get_courses_list_sorted_by_tag():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    courses_list = func_db.execute("""
                                        SELECT *
                                        FROM courses
                                        WHERE visible=1
                                        ORDER BY tag
                                        """
                                             ).fetchall()
    func_db.commit()
    func_db.close()
    return courses_list


def get_courses_list_sorted_by_status():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    courses_list = func_db.execute("""
                                        SELECT *
                                        FROM courses
                                        WHERE visible=1
                                        ORDER BY open DESC
                                        """
                                             ).fetchall()
    func_db.commit()
    func_db.close()
    return courses_list


def search_course_tag(tag):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT tag
                                        FROM courses
                                        WHERE visible=1
                                        AND tag=?
                                    """,
                                     [tag]).fetchall()
    func_db.commit()
    func_db.close()
    return data


def new_studentrole_request(username, message, datetime):
    if message == "":
        message = "-"
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                INSERT INTO StudentRoleRequests
                (username, message, datetime)
                VALUES
                (?, ?, ?)
                """,
                              [username, message, datetime])
    func_db.commit()
    func_db.close()
    return f"New student role request created: {username} / {message} / {datetime}"


def update_studentrole_request(username, message, datetime):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("""
                                UPDATE StudentRoleRequests
                                SET message=?
                                WHERE username=?
                            """,
                              [message, username])
    func_db.execute("""
                                UPDATE StudentRoleRequests
                                SET datetime=?
                                WHERE username=?
                            """,
                              [datetime, username])
    func_db.commit()
    func_db.close()
    return f"Updated student role request: {username} / {message} / {datetime}"


def get_studentrole_requests_list():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    requests = func_db.execute(
        "SELECT * FROM StudentRoleRequests ORDER BY id").fetchall()
    func_db.commit()
    func_db.close()
    return requests


def get_studentrole_requests_list_sorted_by_username():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    requests = func_db.execute("""
                                        SELECT *
                                        FROM StudentRoleRequests
                                        ORDER BY username
                                    """).fetchall()
    func_db.commit()
    func_db.close()
    return requests


def get_studentrole_request_of_user(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    request = func_db.execute("""
                         SELECT *
                         FROM StudentRoleRequests
                         WHERE username=?
                         """,
                                        [username]).fetchall()
    func_db.commit()
    func_db.close()
    return request

def get_all_users_list():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE visible=1
                                    """).fetchall()
    func_db.close()
    return data

def get_all_users_list_sorted_by_name():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE visible=1
                                        ORDER BY username
                                    """).fetchall()
    func_db.close()
    return data

def get_all_users_list_sorted_by_role():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE visible=1
                                        ORDER BY role
                                    """).fetchall()
    func_db.close()
    return data

def get_all_students_list():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=2
                                        AND visible=1
                                    """).fetchall()
    func_db.close()
    return data

def get_all_students_list_sorted_by_name():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=2
                                        AND visible=1
                                        ORDER BY username
                                    """).fetchall()
    func_db.close()
    return data

def get_all_teachers_list():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=1
                                        AND visible=1
                                    """).fetchall()
    func_db.close()
    return data

def get_all_teachers_list_sorted_by_name():
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    data = func_db.execute("""
                                        SELECT *
                                        FROM Users
                                        WHERE role=1
                                        AND visible=1
                                        ORDER BY username
                                    """).fetchall()
    func_db.close()
    return data

def accept_studentrole_request(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute(
        "DELETE FROM StudentRoleRequests WHERE username=?", [username])
    func_db.commit()
    func_db.close()
    set_user_role(username, 2)
    return f"Accepted student role request from {username}"


def reject_studentrole_request(username):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute(
        "DELETE FROM StudentRoleRequests WHERE username=?", [username])
    func_db.commit()
    func_db.close()
    return f"Delete student role request from {username}"


def update_grade(course_tag: str, username: str, grade: int):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("UPDATE InCourse SET grade=? WHERE course_tag=? AND username=?", [grade, course_tag, username])
    func_db.commit()
    func_db.close()
    return f"Updated {username} / {grade} / {course_tag}"

def remove_from_course(course_tag: str, username: str):
    func_db = sqlite3.connect("school.db")
    func_db.isolation_level = None
    func_db.execute("DELETE FROM InCourse WHERE course_tag=? AND username=?", [course_tag, username])
    func_db.commit()
    func_db.close()
    return f"Removed {username} from {course_tag}"