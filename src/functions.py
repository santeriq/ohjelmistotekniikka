from werkzeug.security import check_password_hash
import database


# !! ABOUT COMMENTS !!

# this module has little to no comments
# this is because basically all of the
# are simple


def login(username: str, password: str):
    real_password = database.get_password(username)
    if real_password is not None:
        if check_password_hash(real_password, password):
            return True
        return False
    return None

def new_password(password1: str, password2: str):
    if password1 == password2 and len(password1) >= 8:
        return True
    if password1 != password2 and len(password1) >= 8:
        return False
    return None

def new_username(username: str):
    check = database.search_username(username)
    if len(check) == 0:
        return True
    return False

def new_coursetag(tag: str):
    check = database.search_course_tag(tag)
    if len(check) == 0:
        return True
    return False

def new_role_request(username: str):
    check = database.get_role_request_of_user(username)
    if len(check) == 0:
        return True
    return False

def check_is_user_in_course(username: str, course_tag: str):
    check = database.search_user_in_course(username, course_tag)
    if len(check) == 0:
        return False
    return True

def check_is_course_open(course_tag: str):
    course = database.get_course_info(course_tag)
    if course is None:
        return False
    status = course[4]
    if status == 1:
        return True
    return False
