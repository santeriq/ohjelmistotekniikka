import database
from werkzeug.security import check_password_hash, generate_password_hash


def login(username: str, password: str):
    real_password = database.get_password(username)
    if real_password != None:
        if check_password_hash(database.get_password(username), password):
            return True
        return False
    return None

def new_password(password1: str, password2: str):
    if password1 == password2 and len(password1) >= 8:
        return True
    elif password1 == password2 and len(password1) < 8:
        return None
    elif password1 != password2:
        return False

def new_username(username: str):
    check = database.search_username(username)
    if len(check) == 0:
        return True
    return False

def check_if_course_tag_free(tag: str):
    check = database.search_course_tag(tag)
    if len(check) == 0:
        return True
    return False

def check_if_new_studentrole_request(username: str):
    check = database.get_studentrole_request_of_user(username)
    if len(check) == 0:
        return True
    return False





