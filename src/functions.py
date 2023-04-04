import database
from werkzeug.security import check_password_hash, generate_password_hash



def new_admin(name: str, username: str, password: str):
    database.create_admin(name, username, password)
    return f'Uusi admin luotu nimellä "{username}"'

def new_teacher(name: str, username: str, password: str):
    database.create_teacher(name, username, password)
    return f'Uusi opettaja luotu nimellä "{username}"'

def new_student(name: str, username: str, password: str):
    database.create_student(name, username, password)
    return f'Uusi opiskelija luotu nimellä "{username}"'

def login(username: str, password: str):
    real_password = database.get_password(username)
    if real_password != None:
        if check_password_hash(database.get_password(username), password):
            return True
        return False
    return None





if __name__ == "__main__":
    print(new_admin("Kaaleppi", "admin1", "salasana123"))
    print(new_teacher("Matti", "Matti85", "mattimatti"))
    print(new_teacher("Teppo", "Teppo33", "teppo123"))
    print(new_student("Santeri", "santeri", "santeri321"))
    print(login("admin1", "salasana123")) # True
    print(login("atti85", "mattimatti")) # None / väärä käyttäjätunnus
    print(login("teppo33", "teppo123")) # True
    print(login("SANTERI", "santeri")) # False / väärä salasana
    database.delete_teacher("Teppo33")
    print(login("teppo33", "teppo123")) # None / vääräkäyttäjätunnus
    print(new_teacher("teppo", "Teppo33", "teppo123"))