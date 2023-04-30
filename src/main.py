import gui
import database


# if for some reason there are no admins in the database
# use database.create_admin("{username}", "{password}")
# replace {username} and {password}


database.create_database()
gui.start()
