import database
import functions


# !! NOTICE !!

# database module has no checks
# so be careful when modifying this file


# this is only really for development
# run this file to reset the (ROOT) school.db
# this will not affect the one in (/src)
# the one in /src is only for tests





database.delete_database()
database.create_database()

if True:
    print(database.create_admin("admin1", "password1"))
    print(database.create_teacher("teacher1", "password1"))
    print(database.create_teacher("teacher2", "password1"))
    print(database.create_student("student1", "password1"))
    print(database.create_student("student2", "password1"))
    print(database.create_student("student3", "password1"))
    print(database.create_user("user1", "password1"))
    print(database.create_user("user2", "password1"))
    print(database.create_user("user3", "password1"))
    print(database.create_user("user4", "password1"))
    print(database.create_user("abc", "password1"))
    print(database.create_user("zzz", "password1"))
    print(functions.login("user1", "password1"))  # True
    print(functions.login("user100", "password1")) # None / väärä käyttäjätunnus
    print(functions.login("uSER1", "password1"))  # True
    print(functions.login("user1", "password123"))  # False / väärä salasana
    print(database.delete_teacher("teacher2"))
    print(functions.login("teacher2", "password1")) # None / vääräkäyttäjätunnus
    print(functions.new_username("user1"))  # False / username taken
    print(database.create_course("ohpe2021", "Ohjelmoinnin perusteet 2021", 5))
    print(database.create_course("ohpe2022", "Ohjelmoinnin perusteet 2022", 5))
    print(database.create_course("ohja2021", "Ohjelmoinnin jatkokurssi 2021", 5))
    print(database.create_course("lapio2022", "Tietokone työvälineenä 2022", 1))
    print(database.create_course("tito2022", "Tietokoneen toiminta 2022", 5))
    print(database.close_course("ohpe2021"))
    print(database.close_course("ohpe2021"))
    print(database.create_role_request("user1", "hello world", "13/04/2023 14:48:32"))
    print(database.create_role_request("user2", "", "13/04/2023 14:50:20"))
    print(database.create_role_request("user3", "testing", "14/04/2023 20:10:07"))
    print(database.create_role_request("user4", "testing again", "16/04/2023 10:20:00"))
    print(database.create_role_request("zzz", "hi", "17/08/2023 03:03:30"))
    print(database.create_role_request("abc", "abc", "10/10/2024 10:10:10"))
    print(database.join_course("ohja2021", "teacher1"))
    print(database.join_course("ohja2021", "student1"))
    print(database.join_course("ohja2021", "student2"))
    print(database.join_course("ohja2021", "student3"))
    print(database.update_grade("ohja2021", "student1", 5))
    print(database.update_grade("ohja2021", "student2", 2))