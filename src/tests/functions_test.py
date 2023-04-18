import functions


def test_new_password():
    assert functions.new_password("moi", "moi") == None
    assert functions.new_password("moimoimoi", "moimoi") == False
    assert functions.new_password("moimoimoi", "moimoimoi") == True

def test_login():
    assert functions.login("moi", "moi") == None
    assert functions.login("user1", "moi") == False
    assert functions.login("user1", "salasana1") == True

def test_new_username():
    assert functions.new_username("user1") == False
    assert functions.new_username("moi") == True

def test_new_coursetag():
    assert functions.new_coursetag("ohpe2021") == False
    assert functions.new_coursetag("ohpe2020") == True

def test_new_studentrole_request():
    assert functions.new_studentrole_request("moi") == True
    assert functions.new_studentrole_request("user1") == False
