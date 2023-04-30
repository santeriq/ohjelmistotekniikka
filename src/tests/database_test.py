import database


def test_create_user():
    assert database.create_user("pytestuser1", "password") == "Created new user: pytestuser1"
    assert database.create_user("pytestuser2", "password") == "Created new user: pytestuser2"

def test_create_admin():
    assert database.create_admin("pytestadmin1", "password") == "Created new admin: pytestadmin1"

def test_create_teacher():
    assert database.create_teacher("pytestteacher1", "password") == "Created new teacher: pytestteacher1"
    assert database.create_teacher("pytestteacher2", "password") == "Created new teacher: pytestteacher2"

def test_create_student():
    assert database.create_student("pyteststudent1", "password") == "Created new student: pyteststudent1"

def test_create_course():
    assert database.create_course("pytestcourse1", "pytestcoursename1", 10) == "Created new course: pytestcoursename1 / 10 / pytestcourse1"

def test_close_course():
    assert database.close_course("pytestcourse1") == "Closed course: pytestcourse1"

def test_open_course():
    assert database.open_course("pytestcourse1") == "Opened course: pytestcourse1"

def test_join_course():
    assert database.join_course("pytestcourse1", "pyteststudent1") == "pyteststudent1 joined course pytestcourse1"

def test_leave_course():
    assert database.leave_course("pytestcourse1", "pyteststudent1") == "pyteststudent1 left course pytestcourse1"

def test_delete_teacher():
    assert database.delete_teacher("pytestteacher2") == "Deleted teacher: pytestteacher2"

def test_get_user_role():
    assert database.get_user_role("pytestuser1") == 3
    assert database.get_user_role("pyteststudent1") == 2
    assert database.get_user_role("pytestteacher1") == 1
    assert database.get_user_role("pytestadmin1") == 0

def test_set_user_role():
    assert database.set_user_role("pytestuser2", 0) == "Set pytestuser2 as 0"

def test_create_role_request():
    assert database.create_role_request("pytestuser1", "pytestmessage1", "pytest time 00:01") == "New student role request created: pytestuser1 / pytestmessage1 / pytest time 00:01"

def test_update_role_request():
    assert database.update_role_request("pytestUser1", "pytestMessageUpdate1", "pytest time 00:05") == "Updated student role request: pytestUser1 / pytestMessageUpdate1 / pytest time 00:05"

def test_reject_role_request():
    assert database.reject_role_request("pytestuser1") == "Deleted student role request from pytestuser1"

def test_update_grade():
    assert database.update_grade("pytestcourse1", "pyteststudent1", 1) == "Updated pyteststudent1 / 1 / pytestcourse1"

def test_remove_from_course():
    assert database.remove_from_course("pytestcourse1", "pyteststudent1") == "Removed pyteststudent1 from pytestcourse1"

