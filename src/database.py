import sqlite3
import os
from werkzeug.security import generate_password_hash


# !! ABOUT PYLINT !!

# pylint: disable=invalid-name
# this is because pylint considers "db" as a bad variable name
# but the variable is only used inside functions
# and it shortens the lines


# !! ABOUT COMMENTS !!

# this module has little to no comments
# this is because basically all of the functions are simple



# creating database and deleting it
# creating database and deleting it
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
                            grade INTEGER
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
# database main functions
# database main functions


def create_user(username: str, password: str):
    pw_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
            """,
                [username, pw_hash, 3, 1])
    db.commit()
    db.close()
    return f"Created new user: {username}"


def create_admin(username: str, password: str):
    pw_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
            """,
                [username, pw_hash, 0, 1])
    db.commit()
    db.close()
    return f"Created new admin: {username}"


def create_teacher(username: str, password: str):
    pw_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
            """,
                [username, pw_hash, 1, 1])
    db.commit()
    db.close()
    return f"Created new teacher: {username}"


def create_student(username: str, password: str):
    pw_hash = generate_password_hash(password)
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO Users
                (username, password, role, visible)
                VALUES
                (?, ?, ?, ?)
            """,
                [username, pw_hash, 2, 1])
    db.commit()
    db.close()
    return f"Created new student: {username}"


def create_course(tag: str, name: str, course_credits: int):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO Courses
                (tag, name, credits, open, visible)
                VALUES
                (?, ?, ?, ?, ?)
            """,
                [tag, name, course_credits, 1, 1])
    db.commit()
    db.close()
    return f"Created new course: {name} / {course_credits} / {tag}"


def close_course(tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE courses SET open=0 WHERE tag=?", [tag])
    db.commit()
    db.close()
    return f"Closed course: {tag}"


def open_course(tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE courses SET open=1 WHERE tag=?", [tag])
    db.commit()
    db.close()
    return f"Opened course: {tag}"


def join_course(tag: str, username: str):
    info = get_course_info(tag)
    course_id = info[0]
    course_name = info[2]
    course_credits = info[3]
    user_info = get_user_info(username)
    user_id = user_info[0]
    user_role = user_info[3]
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO InCourse 
                (course_id, course_tag, course_name, course_credits, user_id, username, user_role, grade)
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                [course_id, tag, course_name, course_credits, user_id, username, user_role, 0])
    db.commit()
    db.close()
    return f"{username} joined course {tag}"


def leave_course(tag: str, username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                DELETE FROM InCourse 
                WHERE course_tag=?
                AND username=?
            """,
                [tag, username])
    db.commit()
    db.close()
    return f"{username} left course {tag}"


def delete_teacher(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE users SET visible=0 WHERE username=?", [username])
    db.commit()
    db.close()
    return f"Deleted teacher: {username}"


def get_course_info(tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("SELECT * FROM courses WHERE tag=? AND visible=1", [tag]).fetchone()
    db.close()
    return data


def get_users_in_course(tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("SELECT * FROM InCourse WHERE course_tag=?", [tag]).fetchall()
    db.close()
    return data


def get_students_in_course(tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT username, grade
                        FROM InCourse
                        WHERE course_tag=?
                        AND user_role=2
                        ORDER BY username
                    """,
                        [tag]).fetchall()
    db.close()
    return data


def get_users_courses(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM InCourse
                        WHERE username=?
                        ORDER BY course_name
                    """,
                        [username]).fetchall()
    db.close()
    return data


def search_user_in_course(username: str, course_tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM InCourse
                        WHERE username=?
                        AND course_tag=?
                    """,
                        [username, course_tag]).fetchall()
    db.close()
    return data


def get_user_info(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("SELECT * FROM users WHERE username=? AND visible=1", [username]).fetchone()
    db.close()
    return data


def get_password(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    password = db.execute("""
                            SELECT password
                            FROM users
                            WHERE visible=1
                            AND LOWER(username)=?
                        """,
                            [username.lower()]).fetchone()
    db.close()
    if password is not None:
        return password[0]
    return None


def search_username(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT username
                        FROM users
                        WHERE visible=1
                        AND LOWER(username)=?
                    """,
                        [username.lower()]).fetchall()
    db.close()
    return data


def get_user_role(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT role
                        FROM users
                        WHERE LOWER(username)=?
                    """,
                        [username.lower()]).fetchone()
    db.close()
    return data[0]


def set_user_role(username: str, role: int):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("UPDATE users SET role=? WHERE username=?", [role, username])
    db.commit()
    db.close()
    return f"Set {username} as {role}"


def get_courses_list_sorted_by_name():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT * 
                        FROM courses 
                        WHERE visible=1 
                        ORDER BY name
                    """
                        ).fetchall()
    db.close()
    return data


def get_courses_list_sorted_by_credits():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM courses
                        WHERE visible=1
                        ORDER BY credits DESC
                    """
                        ).fetchall()
    db.close()
    return data


def get_courses_list_sorted_by_tag():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM courses
                        WHERE visible=1
                        ORDER BY tag
                    """
                        ).fetchall()
    db.close()
    return data


def get_courses_list_sorted_by_status():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM courses
                        WHERE visible=1
                        ORDER BY open DESC
                    """
                        ).fetchall()
    db.close()
    return data


def search_course_tag(tag: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT tag
                        FROM courses
                        WHERE visible=1
                        AND tag=?
                    """,
                        [tag]).fetchall()
    db.close()
    return data


def create_role_request(username: str, message: str, time: str):
    if message == "":
        message = "-"
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                INSERT INTO StudentRoleRequests
                (username, message, datetime)
                VALUES
                (?, ?, ?)
            """,
                [username, message, time])
    db.commit()
    db.close()
    return f"New student role request created: {username} / {message} / {time}"


def update_role_request(username: str, message: str, time: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                UPDATE StudentRoleRequests
                SET message=?
                WHERE username=?
            """,
                [message, username])
    db.execute("""
                UPDATE StudentRoleRequests
                SET datetime=?
                WHERE username=?
            """,
                [time, username])
    db.commit()
    db.close()
    return f"Updated student role request: {username} / {message} / {time}"


def get_role_requests_list():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    requests = db.execute("SELECT * FROM StudentRoleRequests ORDER BY id").fetchall()
    db.close()
    return requests


def get_role_requests_list_sorted_by_username():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM StudentRoleRequests
                        ORDER BY username
                    """
                        ).fetchall()
    db.close()
    return data


def get_role_request_of_user(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM StudentRoleRequests
                        WHERE username=?
                    """,
                        [username]).fetchall()
    db.close()
    return data


def get_all_users_list():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE visible=1
                    """
                        ).fetchall()
    db.close()
    return data


def get_all_users_list_sorted_by_name():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE visible=1
                        ORDER BY username
                    """
                        ).fetchall()
    db.close()
    return data


def get_all_users_list_sorted_by_role():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE visible=1
                        ORDER BY role
                    """
                        ).fetchall()
    db.close()
    return data


def get_all_students_list():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE role=2
                        AND visible=1
                    """
                        ).fetchall()
    db.close()
    return data


def get_all_students_list_sorted_by_name():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE role=2
                        AND visible=1
                        ORDER BY username
                    """
                        ).fetchall()
    db.close()
    return data


def get_all_teachers_list():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE role=1
                        AND visible=1
                    """
                        ).fetchall()
    db.close()
    return data

def get_all_teachers_list_sorted_by_name():
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM Users
                        WHERE role=1
                        AND visible=1
                        ORDER BY username
                    """
                        ).fetchall()
    db.close()
    return data


def accept_role_request(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("DELETE FROM StudentRoleRequests WHERE username=?", [username])
    db.commit()
    db.close()
    set_user_role(username, 2)
    return f"Accepted student role request from {username}"


def reject_role_request(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("DELETE FROM StudentRoleRequests WHERE username=?", [username])
    db.commit()
    db.close()
    return f"Deleted student role request from {username}"


def update_grade(tag: str, username: str, grade: int):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("""
                UPDATE InCourse
                SET grade=?
                WHERE course_tag=?
                AND username=?
            """,
                [grade, tag, username])
    db.commit()
    db.close()
    return f"Updated {username} / {grade} / {tag}"


def remove_from_course(tag: str, username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    db.execute("DELETE FROM InCourse WHERE course_tag=? AND username=?", [tag, username])
    db.commit()
    db.close()
    return f"Removed {username} from {tag}"


def get_student_credits(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT SUM(course_credits)
                        FROM InCourse
                        WHERE username=?
                        AND grade>0
                    """,
                        [username]).fetchone()
    db.close()
    return data[0]


def get_student_gpa(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    grades_sum = db.execute("""
                            SELECT SUM(grade)
                            FROM InCourse
                            WHERE username=?
                            AND grade>0
                        """,
                            [username]).fetchone()
    courses = db.execute("""
                            SELECT COUNT(*)
                            FROM InCourse
                            WHERE username=?
                            AND grade>0
                        """,
                            [username]).fetchone()
    db.close()
    if grades_sum[0] is not None and courses[0] is not None:
        gpa = grades_sum[0]/courses[0]
    else:
        gpa = None
    return gpa


def get_student_credits_list(username: str):
    db = sqlite3.connect("school.db")
    db.isolation_level = None
    data = db.execute("""
                        SELECT *
                        FROM InCourse
                        WHERE username=?
                        AND grade>0
                        ORDER BY grade DESC
                    """,
                        [username]).fetchall()
    db.close()
    return data
