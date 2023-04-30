import functions


def test_new_password():
    assert functions.new_password("moi", "moi") == None
    assert functions.new_password("moimoimoi", "moimoi") == False
    assert functions.new_password("moimoimoi", "moimoimoi") == True

def test_login():
    assert functions.login("moi", "moi") == None
    assert functions.login("user1", "moi") == False
    assert functions.login("user1", "password1") == True

def test_new_username():
    assert functions.new_username("user1") == False
    assert functions.new_username("moi") == True

def test_new_coursetag():
    assert functions.new_coursetag("ohpe2021") == False
    assert functions.new_coursetag("ohpe2020") == True

def test_new_role_request():
    assert functions.new_role_request("moi") == True
    assert functions.new_role_request("user1") == False
    assert functions.new_role_request("hdhgsadgjgd") == True

def test_check_is_user_in_course():
    assert functions.check_is_user_in_course("student1", "ohja2021") == True
    assert functions.check_is_user_in_course("student1", "ohja2024") == False
    assert functions.check_is_user_in_course("hasdhsadada", "ohja2024") == False
    assert functions.check_is_user_in_course("student1", "hjdhjsagg") == False

def test_check_is_course_open():
    assert functions.check_is_course_open("ohja2021") == True
    assert functions.check_is_course_open("ohpe2021") == False
    assert functions.check_is_course_open("dsakjdsa") == False


