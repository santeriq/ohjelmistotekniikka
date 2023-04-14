import gui
import database
import functions


# you only have to run this 
# gui.py has function that will start the program
# when running first time you should close the program
# after closing the program if-statement will run and add testing accounts
# you should change True value to False not to make duplicates in database
# to erase the database use function database.delete_database()


if True:
    print(database.create_admin("admin1", "salasana1"))
    print(database.create_teacher("teacher1", "salasana1"))
    print(database.create_teacher("teacher2", "salasana1"))
    print(database.create_student("student1", "salasana1"))
    print(database.create_user("user1", "salasana1"))
    print(database.create_user("user2", "salasana1"))
    print(database.create_user("user3", "salasana1"))
    print(database.create_user("user4", "salasana1"))
    print(database.create_user("abc", "salasana1"))
    print(database.create_user("zzz", "salasana1"))
    print(functions.login("user1", "salasana1")) # True
    print(functions.login("user100", "salasana1")) # None / väärä käyttäjätunnus
    print(functions.login("uSER1", "salasana1")) # True
    print(functions.login("user1", "salasana123")) # False / väärä salasana
    print(database.delete_teacher("teacher1"))
    print(functions.login("teacher1", "salasana1")) # None / vääräkäyttäjätunnus
    print(functions.new_username("user1")) # False / username taken
    print(database.create_course("ohpe2021", "Ohjelmoinnin perusteet 2021", 5)) 
    print(database.create_course("ohpe2022", "Ohjelmoinnin perusteet 2022", 5)) 
    print(database.create_course("ohja2021", "Ohjelmoinnin jatkokurssi 2021", 5))
    print(database.create_course("lapio2022", "Tietokone työvälineenä 2022", 1))
    print(database.create_course("tito2022", "Tietokoneen toiminta 2022", 5))
    print(database.close_course("ohpe2021"))
    print(database.close_course("ohpe2021"))
    print(database.new_studentrole_request("user1", "hello world", "13/04/2023 14:48:32"))
    print(database.new_studentrole_request("user2", "", "13/04/2023 14:50:20"))
    print(database.new_studentrole_request("user3", "testing", "14/04/2023 20:10:07"))
    print(database.new_studentrole_request("user4", "testing again", "16/04/2023 10:20:00"))
    print(database.new_studentrole_request("zzz", "hi", "17/08/2023 03:03:30"))
    print(database.new_studentrole_request("abc", "abc", "10/10/2024 10:10:10"))