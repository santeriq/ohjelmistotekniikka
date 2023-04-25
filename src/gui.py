from tkinter import Tk, Frame, Label, Button, Entry, Canvas, Toplevel, Radiobutton, StringVar, IntVar
from tkinter import N, Y, RIGHT, VERTICAL, BOTH, LEFT
from tkinter import ttk
from datetime import datetime
import database
import functions

def start():
    global root
    root = Tk()
    root.title("vilma")
    root.geometry("600x400")

    global frame
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=1)

    global FONT
    FONT = "Courier"

    main_screen()
    root.mainloop()


# helpful functions

def clear_frame():
    for widgets in frame.winfo_children():
        widgets.destroy()


def clear_popup():
    for widgets in popup.winfo_children():
        widgets.destroy()


def add_scrollbar_to_right():
    global second_frame
    popup_frame = Frame(popup)
    popup_frame.pack(fill=BOTH, expand=1)
    popup_canvas = Canvas(popup_frame)
    popup_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    popup_scrollbar = ttk.Scrollbar(popup_frame, orient=VERTICAL, command=popup_canvas.yview)
    popup_scrollbar.pack(side=RIGHT, fill=Y)
    popup_canvas.configure(yscrollcommand=popup_scrollbar.set)
    popup_canvas.bind("<Configure>", lambda e: popup_canvas.configure(scrollregion=popup_canvas.bbox("all")))
    second_frame = Frame(popup_canvas)
    popup_canvas.create_window((0, 0), window=second_frame, anchor="nw")


# main screen and login / account creation


def main_screen():
    clear_frame()
    Label(frame, text="Welcome to Vilma", font=(FONT, 25)).place(x=120, y=120)
    Button(frame, text="Already have an account?", bd=3, command=login).place(x=140, y=160)
    Button(frame, text="Create account", command=create_account).place(x=320, y=160)


def login():
    clear_frame()
    Label(frame, text="------------------------------------------------------------------").place(x=100, y=40)
    Label(frame, text="username", padx=10, width=17).place(x=100, y=60)
    Label(frame, text="password", padx=10, width=17).place(x=100, y=80)
    username = Entry(frame, width=30)
    username.place(x=240, y=60)
    password = Entry(frame, width=30, show="*")
    password.place(x=240, y=80)
    Label(frame, text="------------------------------------------------------------------").place(x=100, y=100)
    Button(frame, text="Log in", bd=3, width=15, command=lambda: login_check(username.get(), password.get())).place(x=300, y=120)
    Button(frame, text="Back", command=main_screen, width=10).place(x=450, y=30)


def login_check(username, password):
    clear_frame()
    login()
    correct = functions.login(username, password)
    if correct is None:
        Label(frame, text="Username not found", font=(FONT, 8, "bold")).place(x=440, y=60)
    elif correct is False:
        Label(frame, text="Wrong password", font=(FONT, 8, "bold")).place(x=450, y=80)
    elif correct is True:
        logged_in(username)


def create_account():
    clear_frame()
    Label(frame, text="------------------------------------------------------------------").place(x=100, y=40)
    Label(frame, text="username", padx=10, width=17).place(x=100, y=60)
    Label(frame, text="password", padx=10, width=17).place(x=100, y=80)
    Label(frame, text="password again", padx=10, width=17).place(x=100, y=100)
    username = Entry(frame, width=30)
    username.place(x=240, y=60)
    password1 = Entry(frame, width=30, show="*")
    password1.place(x=240, y=80)
    password2 = Entry(frame, width=30, show="*")
    password2.place(x=240, y=100)
    Label(frame, text="------------------------------------------------------------------").place(x=100, y=120)
    Button(frame, text="Create account", bd=3, width=15, command=lambda: create_account_check(username.get(), password1.get(), password2.get())).place(x=300, y=140)
    Button(frame, text="Back", command=main_screen, width=10).place(x=450, y=30)


def create_account_check(username_input, password1_input, password2_input):
    clear_frame()
    Label(frame, text="------------------------------------------------------------------").place(x=100, y=40)
    Label(frame, text="username", padx=10, width=17).place(x=100, y=60)
    Label(frame, text="password", padx=10, width=17).place(x=100, y=80)
    Label(frame, text="password again", padx=10, width=17).place(x=100, y=100)
    username = Entry(frame, width=30)
    username.insert(0, username_input)
    username.place(x=240, y=60)
    password1 = Entry(frame, width=30, show="*")
    password1.place(x=240, y=80)
    password2 = Entry(frame, width=30, show="*")
    password2.place(x=240, y=100)
    Label(frame, text="------------------------------------------------------------------").place(x=100, y=120)
    Button(frame, text="Create account", bd=3, width=15, command=lambda: create_account_check(username.get(), password1.get(), password2.get())).place(x=100, y=140)
    Button(frame, text="Back", command=main_screen, width=10).place(x=450, y=30)

    new_password = functions.new_password(password1_input, password2_input)
    new_username = functions.new_username(username_input)
    if new_username and new_password:
        database.create_user(username_input, password1_input)
        logged_in(username_input)
    elif new_username is False:
        Label(frame, text="Username is taken", font=(FONT, 8, "bold")).place(x=440, y=60)
    elif new_password is False:
        Label(frame, text="Wrong password", font=(FONT, 8, "bold")).place(x=450, y=100)
    elif new_password is None:
        Label(frame, text="Password too short", font=(FONT, 8, "bold")).place(x=440, y=80)
        Label(frame, text="Minimum 8 characters", font=(FONT, 8, "bold")).place(x=440, y=100)


# screens of different users logged in


def logged_in(username):
    clear_frame()
    user_role = database.get_user_role(username)
    if user_role == 2:
        logged_in_as_student(username)
    elif user_role == 1:
        logged_in_as_teacher(username)
    elif user_role == 0:
        logged_in_as_admin(username)
    elif user_role == 3:
        logged_in_as_none(username)

def logged_in_as_none(username):
    Button(frame, text="Log out", command=main_screen, bd=3).place(x=545, y=0)
    Label(frame, text=f"You are now logged in as {username}").place(x=200, y=0)
    Label(frame, text="(request a role from either a teacher or an admin)", font=(FONT, 9, "bold")).place(x=125, y=18)
    Label(frame, text="Your message (optional)").place(x=30, y=100)
    Label(frame, text="max 30 characters").place(x=50, y=120)
    message_box = Entry(frame, width=60)
    message_box.place(x=175, y=100)
    Button(frame, text="Request\nstudent role", command=lambda: request_student_role(username, message_box.get()), bd=3, width=20).place(x=390, y=130)

def logged_in_as_student(username):
    Button(frame, text="Log out", command=main_screen, bd=3).place(x=545, y=0)
    Label(frame, text="You are now logged in as").place(x=100, y=0)
    Label(frame, text=f"{username} (student)", font=(FONT, 9, "bold")).place(x=238, y=0)

def logged_in_as_teacher(username):
    Button(frame, text="Log out", command=main_screen, bd=3).place(x=545, y=0)
    Label(frame, text="You are now logged in as").place(x=100, y=0)
    Label(frame, text=f"{username} (teacher)",
          font=(FONT, 9, "bold")).place(x=238, y=0)

def logged_in_as_admin(username):
    Button(frame, text="Log out", command=main_screen, bd=3).place(x=545, y=0)
    Label(frame, text="You are now logged in as").place(x=100, y=0)
    Label(frame, text=f"{username} (admin)", font=(FONT, 9, "bold")).place(x=238, y=0)
    Button(frame, text="Create new course", command=create_course, width=14, bd=3, pady=3).place(x=100, y=100)
    Button(frame, text="Open course", command=open_course, width=14, pady=3).place(x=100, y=131)
    Button(frame, text="Close course", command=close_course, width=14).place(x=100, y=160)
    Button(frame, text="View courses", command=create_view_courses_popup, width=14, bd=3, pady=3).place(x=100, y=250)
    Button(frame, text="Control roles", command=control_roles_as_admin, width=14, bd=3, pady=3).place(x=250, y=100)
    Button(frame, text="View all users", command=create_view_all_users_popup, width=14, bd=3, pady=3).place(x=250, y=250)
    Button(frame, text="View students", command=create_view_all_students_popup, width=14, bd=3, pady=3).place(x=250, y=280)
    Button(frame, text="View teachers", command=create_view_all_teachers_popup,width=14, bd=3, pady=3).place(x=250, y=310)
    Button(frame, text="View student role requests", command=create_view_student_requests_popup, width=25, bd=3, pady=3).place(x=100, y=350)


# role "guest" functionality


def request_student_role(username, message):
    clear_frame()
    logged_in_as_none(username)
    new_request = functions.new_studentrole_request(username)
    datetime_now = datetime.now()
    datetime_string = datetime_now.strftime("%d/%m/%Y %H:%M:%S")
    if new_request and len(message) <= 30:
        database.new_studentrole_request(username, message, datetime_string)
        Label(frame, text="Your request has been sent", font=(FONT, 8, "bold")).place(x=175, y=140)
    elif new_request is False and len(message) <= 30:
        database.update_studentrole_request(username, message, datetime_string)
        Label(frame, text="Your request has been updated", font=(FONT, 8, "bold")).place(x=175, y=140)
    elif len(message) > 30:
        Label(frame, text="Your message is too long", font=(FONT, 8, "bold")).place(x=175, y=140)


# student tools


# teacher tools


# admin tools

def create_view_all_users_popup():
    global popup
    popup = Toplevel(root)
    popup.geometry("430x400")
    popup.title("View all users")
    view_all_users()

def view_all_users():
    global users_list
    users_list = database.get_all_users_list()
    update_view_all_users()

def view_all_users_by_name():
    global users_list
    users_list = database.get_all_users_list_sorted_by_name()
    update_view_all_users()

def view_all_users_by_role():
    global users_list
    users_list = database.get_all_users_list_sorted_by_role()
    update_view_all_users()

def update_view_all_users():
    clear_popup()
    add_scrollbar_to_right()
    Label(second_frame, text="id").grid(row=0, column=1)
    Label(second_frame, text="username").grid(row=0, column=2)
    Label(second_frame, text="role").grid(row=0, column=3)
    Label(second_frame, text="Order by").grid(row=1, column=0)
    Button(second_frame, text="Default", command=view_all_users, width=15).grid(row=1, column=1)
    Button(second_frame, text="x", command=view_all_users_by_name, width=15).grid(row=1, column=2)
    Button(second_frame, text="x",command=view_all_users_by_role , width=15).grid(row=1, column=3)
    row = 2
    column = 1
    for user in users_list:
        id = user[0]
        username = user[1]
        role = user[3]
        if role == 0:
            role = "admin"
        elif role == 1:
            role = "teacher"
        elif role == 2:
            role = "student"
        elif role == 3:
            role = "none"
        Label(second_frame, text=f"{id}").grid(row=row, column=column, sticky=N)
        Label(second_frame, text=f"{username}").grid(row=row, column=column+1, sticky=N)
        Label(second_frame, text=f"{role}").grid(row=row, column=column+2, sticky=N)
        row = row + 1

def create_view_all_students_popup():
    global popup
    popup = Toplevel(root)
    popup.geometry("430x400")
    popup.title("View all students")
    view_all_students()

def view_all_students():
    global students_list
    students_list = database.get_all_students_list()
    update_view_all_students()

def view_all_students_by_name():
    global students_list
    students_list = database.get_all_students_list_sorted_by_name()
    update_view_all_students()

def update_view_all_students():
    clear_popup()
    add_scrollbar_to_right()
    Label(second_frame, text="id").grid(row=0, column=1)
    Label(second_frame, text="username").grid(row=0, column=2)
    Label(second_frame, text="role").grid(row=0, column=3)
    Label(second_frame, text="Order by").grid(row=1, column=0)
    Button(second_frame, text="Default", command=view_all_students, width=15).grid(row=1, column=1)
    Button(second_frame, text="x", command=view_all_students_by_name, width=15).grid(row=1, column=2)
    Button(second_frame, text="x",command=view_all_students , width=15).grid(row=1, column=3)
    row = 2
    column = 1
    for student in students_list:
        id = student[0]
        username = student[1]
        role = "student"
        Label(second_frame, text=f"{id}").grid(row=row, column=column, sticky=N)
        Label(second_frame, text=f"{username}").grid(row=row, column=column+1, sticky=N)
        Label(second_frame, text=f"{role}").grid(row=row, column=column+2, sticky=N)
        row = row + 1

def create_view_all_teachers_popup():
    global popup
    popup = Toplevel(root)
    popup.geometry("430x400")
    popup.title("View all teachers")
    view_all_teachers()

def view_all_teachers():
    global teachers_list
    teachers_list = database.get_all_teachers_list()
    update_view_all_teachers()

def view_all_teachers_by_name():
    global teachers_list
    teachers_list = database.get_all_teachers_list_sorted_by_name()
    update_view_all_teachers()

def update_view_all_teachers():
    clear_popup()
    add_scrollbar_to_right()
    Label(second_frame, text="id").grid(row=0, column=1)
    Label(second_frame, text="username").grid(row=0, column=2)
    Label(second_frame, text="role").grid(row=0, column=3)
    Label(second_frame, text="Order by").grid(row=1, column=0)
    Button(second_frame, text="Default", command=view_all_teachers, width=15).grid(row=1, column=1)
    Button(second_frame, text="x", command=view_all_teachers_by_name, width=15).grid(row=1, column=2)
    Button(second_frame, text="x",command=view_all_teachers , width=15).grid(row=1, column=3)
    row = 2
    column = 1
    for teacher in teachers_list:
        id = teacher[0]
        username = teacher[1]
        role = "teacher"
        Label(second_frame, text=f"{id}").grid(row=row, column=column, sticky=N)
        Label(second_frame, text=f"{username}").grid(row=row, column=column+1, sticky=N)
        Label(second_frame, text=f"{role}").grid(row=row, column=column+2, sticky=N)
        row = row + 1


def create_view_student_requests_popup():
    global popup
    popup = Toplevel(root)
    popup.geometry("900x400")
    popup.title("View student role requests")
    view_student_requests()


def view_student_requests():
    global requests_list
    requests_list = database.get_studentrole_requests_list()
    update_view_student_requests_popup()


def view_student_requests_default():
    global requests_list
    requests_list = database.get_studentrole_requests_list()
    update_view_student_requests_popup()


def accept_student_request_from_default(username):
    database.accept_studentrole_request(username)
    global requests_list
    requests_list = database.get_studentrole_requests_list()
    update_view_student_requests_popup()


def reject_student_request_from_default(username):
    database.reject_studentrole_request(username)
    global requests_list
    requests_list = database.get_studentrole_requests_list()
    update_view_student_requests_popup()


def view_student_requests_sorted():
    global requests_list
    requests_list = database.get_studentrole_requests_list_sorted_by_username()
    update_view_student_requests_popup_sorted()


def accept_student_request_from_sorted(username):
    database.accept_studentrole_request(username)
    global requests_list
    requests_list = database.get_studentrole_requests_list_sorted_by_username()
    update_view_student_requests_popup_sorted()


def reject_student_request_from_sorted(username):
    database.reject_studentrole_request(username)
    global requests_list
    requests_list = database.get_studentrole_requests_list_sorted_by_username()
    update_view_student_requests_popup_sorted()


def update_view_student_requests_popup():
    clear_popup()
    add_scrollbar_to_right()
    Label(second_frame, text="Date-time").grid(row=0, column=1)
    Label(second_frame, text="Username").grid(row=0, column=2)
    Label(second_frame, text="Message", width=50).grid(row=0, column=3)
    Label(second_frame, text="Approve request").grid(row=0, column=4, columnspan=2, sticky=N)
    Label(second_frame, text="Order by").grid(row=1, column=0)
    Button(second_frame, text="Oldest",command=view_student_requests_default, width=25).grid(row=1, column=1)
    Button(second_frame, text="x", command=view_student_requests_sorted, width=15).grid(row=1, column=2)
    row = 2
    column = 1
    username_dict = {}
    row_username_list = 2
    for request in requests_list:
        username_dict[row_username_list] = request[1]
        row_username_list = row_username_list + 1
    for request in requests_list:
        username = request[1]
        message = request[2]
        time = request[3]
        Label(second_frame, text=f"{time}").grid(row=row, column=column, sticky=N)
        Label(second_frame, text=f"{username}").grid(row=row, column=column+1, sticky=N)
        Label(second_frame, text=f"{message}").grid(row=row, column=column+2, sticky=N)
        accept_button = Button(second_frame, text="Accept", command=lambda row2=row: accept_student_request_from_default(username_dict[row2]), width=10, bd=3)
        accept_button.grid(row=row, column=column+3, sticky=N, padx=(0, 5))
        reject_button = Button(second_frame, text="Reject", command=lambda row2=row: reject_student_request_from_default(username_dict[row2]), width=10)
        reject_button.grid(row=row, column=column+4, sticky=N, padx=(5, 0))
        row = row + 1


def update_view_student_requests_popup_sorted():
    clear_popup()
    add_scrollbar_to_right()
    Label(second_frame, text="Date-time").grid(row=0, column=1)
    Label(second_frame, text="Username").grid(row=0, column=2)
    Label(second_frame, text="Message", width=50).grid(row=0, column=3)
    Label(second_frame, text="Approve request").grid(row=0, column=4, columnspan=2, sticky=N)
    Label(second_frame, text="Order by").grid(row=1, column=0)
    Button(second_frame, text="Oldest",command=view_student_requests_default, width=25).grid(row=1, column=1)
    Button(second_frame, text="x", command=view_student_requests_sorted, width=15).grid(row=1, column=2)
    row = 2
    column = 1
    username_dict = {}
    row_username_list = 2
    for request in requests_list:
        username_dict[row_username_list] = request[1]
        row_username_list = row_username_list + 1
    for request in requests_list:
        username = request[1]
        message = request[2]
        time = request[3]
        Label(second_frame, text=f"{time}").grid(row=row, column=column, sticky=N)
        Label(second_frame, text=f"{username}").grid(row=row, column=column+1, sticky=N)
        Label(second_frame, text=f"{message}").grid(row=row, column=column+2, sticky=N)
        accept_button = Button(second_frame, text="Accept", command=lambda row2=row: accept_student_request_from_sorted(username_dict[row2]), width=10, bd=3)
        accept_button.grid(row=row, column=column+3, sticky=N, padx=(0, 5))
        reject_button = Button(second_frame, text="Reject", command=lambda row2=row: reject_student_request_from_sorted(username_dict[row2]), width=10)
        reject_button.grid(row=row, column=column+4, sticky=N, padx=(5, 0))
        row = row + 1


def control_roles_as_admin():
    global popup
    popup = Toplevel(root)
    popup.geometry("210x210")
    popup.title("Assign role")
    Label(popup, text="Assign role", font=15).pack()
    Label(popup, text="Username").place(x=0, y=40)
    username_entry = Entry(popup, width=18)
    username_entry.place(x=70, y=40)
    role = IntVar()
    role.set(2)
    Radiobutton(popup, text="Student", variable=role, value=2).place(x=80, y=60)
    Radiobutton(popup, text="Teacher", variable=role, value=1).place(x=80, y=80)
    Radiobutton(popup, text="Admin", variable=role, value=0).place(x=80, y=100)
    Radiobutton(popup, text="None", variable=role, value=3).place(x=80, y=120)
    Button(popup, text="Confirm", command=lambda: control_roles_as_admin_check(username_entry.get(), role.get())).place(x=80, y=150)


def control_roles_as_admin_check(username_input, role_input):
    clear_popup()
    Label(popup, text="Assign role", font=15).pack()
    Label(popup, text="Username").place(x=0, y=40)
    username_entry = Entry(popup, width=18)
    username_entry.place(x=70, y=40)
    role = IntVar()
    role.set(2)
    Radiobutton(popup, text="Student", variable=role, value=2).place(x=80, y=60)
    Radiobutton(popup, text="Teacher", variable=role, value=1).place(x=80, y=80)
    Radiobutton(popup, text="Admin", variable=role, value=0).place(x=80, y=100)
    Radiobutton(popup, text="None", variable=role, value=3).place(x=80, y=120)
    Button(popup, text="Confirm", command=lambda: control_roles_as_admin_check(username_entry.get(), role.get())).place(x=80, y=150)
    username_not_found = functions.new_username(username_input)
    if username_not_found is True:
        Label(popup, text="Username was not found", font=(FONT, 8, "bold")).place(x=20, y=180)
    else:
        if role_input == 0:
            role_str = "admin"
        elif role_input == 1:
            role_str = "teacher"
        elif role_input == 2:
            role_str = "student"
        elif role_input == 3:
            role_str = "none"
        database.set_user_role(username_input, role_input)
        Label(popup, text=f'Set "{username_input}" as {role_str}\nyou can now close the window', font=(FONT, 8, "bold")).place(x=0, y=180)


def create_course():
    global popup
    popup = Toplevel(root)
    popup.geometry("210x190")
    popup.title("Create course")
    Label(popup, text="Create new course", font=15).pack()
    Label(popup, text="Name").place(x=0, y=40)
    Label(popup, text="Credits").place(x=0, y=60)
    Label(popup, text="Tag").place(x=0, y=80)
    name_entry = Entry(popup, width=23)
    name_entry.place(x=50, y=40)
    credits_enty = Entry(popup, width=23)
    credits_enty.place(x=50, y=60)
    tag_entry = Entry(popup, width=23)
    tag_entry.place(x=50, y=80)
    Button(popup, text="Confirm", width=20, command=lambda: create_course_check(tag_entry.get(), name_entry.get(), credits_enty.get())).place(x=25, y=120)


def create_course_check(tag, name, credits_input):
    clear_popup()
    Label(popup, text="Create new course", font=15).pack()
    Label(popup, text="Name").place(x=0, y=40)
    Label(popup, text="Credits").place(x=0, y=60)
    Label(popup, text="Tag").place(x=0, y=80)
    name_entry = Entry(popup, width=23)
    name_entry.place(x=50, y=40)
    credits_enty = Entry(popup, width=23)
    credits_enty.place(x=50, y=60)
    tag_entry = Entry(popup, width=23)
    tag_entry.place(x=50, y=80)
    Button(popup, text="Confirm", width=20, command=lambda: create_course_check(tag_entry.get(), name_entry.get(), credits_enty.get())).place(x=25, y=120)

    tag = tag.lower()
    if len(name) < 5:
        Label(popup, text="Course name must be at\n least 5 characters long", font=(FONT, 8, "bold")).place(x=15, y=150)
    elif len(tag) < 3:
        Label(popup, text="Course tag must be at\nleast 3 characters long", font=(FONT, 8, "bold")).place(x=15, y=150)
    elif functions.new_coursetag(tag) is True and credits_input.isdigit() is True:
        database.create_course(tag, name, credits_input)
        Label(popup, text="New course has been created,\nyou can now close the window", font=(FONT, 8, "bold")).place(x=0, y=150)
    elif functions.new_coursetag(tag) is True and credits_input.isdigit() is False:
        Label(popup, text="Credits must be an integer", font=(FONT, 8, "bold")).place(x=10, y=150)
    elif functions.new_coursetag(tag) is False and credits_input.isdigit() is True:
        Label(popup, text=f'Course tag must be unique,\n"{tag}" is already in use', font=(FONT, 8, "bold")).place(x=0, y=150)


def create_view_courses_popup():
    global popup
    popup = Toplevel(root)
    popup.geometry("650x400")
    popup.title("View courses")
    update_view_courses_popup(database.get_courses_list_sorted_by_name())


def update_view_courses_popup(courses_list):
    clear_popup()
    add_scrollbar_to_right()
    Label(second_frame, text="Course name").grid(row=0, column=1)
    Label(second_frame, text="credits").grid(row=0, column=2)
    Label(second_frame, text="tag").grid(row=0, column=3)
    Label(second_frame, text="open").grid(row=0, column=4)
    Label(second_frame, text="Order by").grid(row=1, column=0)
    Button(second_frame, text="Default", width=25, command=lambda: update_view_courses_popup(database.get_courses_list_sorted_by_name())).grid(row=1, column=1)
    Button(second_frame, text="x", width=15, command=lambda: update_view_courses_popup(database.get_courses_list_sorted_by_credits())).grid(row=1, column=2)
    Button(second_frame, text="x", width=15, command=lambda: update_view_courses_popup(database.get_courses_list_sorted_by_tag())).grid(row=1, column=3)
    Button(second_frame, text="x", width=15, command=lambda: update_view_courses_popup(database.get_courses_list_sorted_by_status())).grid(row=1, column=4)
    row = 2
    column = 1
    for course in courses_list:
        tag = course[1]
        name = course[2]
        credits_func = course[3]
        open_func = course[4]
        if open_func == 1:
            open_func = "Open"
        elif open_func == 0:
            open_func = "Closed"
        Label(second_frame, text=f"{name}       ").grid(row=row, column=column, sticky=N)
        Label(second_frame, text=f"{credits_func}").grid(row=row, column=column+1, sticky=N)
        Label(second_frame, text=f"       {tag}       ").grid(row=row, column=column+2, sticky=N)
        Label(second_frame, text=f"{open_func}").grid(row=row, column=column+3, sticky=N)
        row = row + 1


def open_course():
    global popup
    popup = Toplevel(root)
    popup.geometry("210x190")
    popup.title("Open course")
    Label(popup, text="Open course", font=15).pack()
    Label(popup, text="Course tag").place(x=0, y=40)
    tag_entry = Entry(popup, width=18)
    tag_entry.place(x=70, y=40)
    Button(popup, text="Confirm", width=20, command=lambda: open_course_tag_check(tag_entry.get())).place(x=25, y=80)


def close_course():
    global popup
    popup = Toplevel(root)
    popup.geometry("210x190")
    popup.title("Close course")
    Label(popup, text="Close course", font=15).pack()
    Label(popup, text="Course tag").place(x=0, y=40)
    tag_entry = Entry(popup, width=18)
    tag_entry.place(x=70, y=40)
    Button(popup, text="Confirm", width=20, command=lambda: close_course_tag_check(tag_entry.get())).place(x=25, y=80)


def close_course_tag_check(tag):
    clear_popup()
    Label(popup, text="Close course", font=15).pack()
    Label(popup, text="Course tag").place(x=0, y=40)
    tag_entry = Entry(popup, width=18)
    tag_entry.place(x=70, y=40)
    Button(popup, text="Confirm", width=20, command=lambda: close_course_tag_check(tag_entry.get())).place(x=25, y=80)

    tag = tag.lower()
    if functions.new_coursetag(tag) is False:
        database.close_course(tag)
        Label(popup, text="Course has been closed,\nyou can now close the window", font=(FONT, 8, "bold")).place(x=0, y=120)
    else:
        Label(popup, text="Could not find course\nmatching with that tag", font=(FONT, 8, "bold")).place(x=20, y=120)


def open_course_tag_check(tag):
    clear_popup()
    Label(popup, text="Open course", font=15).pack()
    Label(popup, text="Course tag").place(x=0, y=40)
    tag_entry = Entry(popup, width=18)
    tag_entry.place(x=70, y=40)
    Button(popup, text="Confirm", width=20, command=lambda: open_course_tag_check(tag_entry.get())).place(x=25, y=80)

    tag = tag.lower()
    if functions.new_coursetag(tag) is False:
        database.open_course(tag)
        Label(popup, text="Course has been opened,\nyou can now close the window", font=(FONT, 8, "bold")).place(x=0, y=120)
    else:
        Label(popup, text="Could not find course\nmatching with that tag", font=(FONT, 8, "bold")).place(x=20, y=120)
