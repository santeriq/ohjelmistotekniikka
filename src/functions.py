from werkzeug.security import check_password_hash
import database


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

def new_studentrole_request(username: str):
    check = database.get_studentrole_request_of_user(username)
    if len(check) == 0:
        return True
    return False
