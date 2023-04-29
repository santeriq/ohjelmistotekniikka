14.4.2023 perjantai:

GUI tehty tkinter avulla

luotu neljä eri käyttäjäroolia: none (guest), student, teacher, admin

role none:
 - mahdollista lähettää opiskelijarooli pyyntö
 
role admin:
 - mahdollista hyväksyä opiskelijarooli pyyntö
 - mahdollista jakaa rooleja käyttäjänimen avulla
 - mahdollista luoda uusi kurssi
 - mahdollista sulkea kurssi
 - mahdollista avata kurssi
 - mahdollista selata kursseja läpi

---------------------

25.4.2023 tiistai:

Database muutos
 - roolit vaihdettiin numeroiksi 0-3

role admin:
 - lisätty "view users"
 - lisätty "view students"
 - lisätty "view teachers"
 - poistettu "delete users"


---------------------

29.4.2023 lauantai:

Database muutos
 - uusi taulukko

role teacher:
 - lisätty "join course"
 - lisätty "leave course"
 - lisätty "view my courses"
 - lisätty "view all courses"
 - lisätty "give grade"
 - lisätty "remove student"
 - lisätty "view student role requests"

role student:
 - lisätty "join course"
 - lisätty "leave course"
 - lisätty "view my courses"
 - lisätty "view all courses"
 - lisätty "view my credits"