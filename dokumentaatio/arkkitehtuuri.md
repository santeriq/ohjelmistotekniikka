Rakenne
------------------------------------
Sovelluksen rakenne on kieltämättä hieman kehno.

- sovelluksen käyttämä school.db sijaitsee rootissa tasks.py README.md kanssa
- src hakemistossa on toinen school.db jota käytetään testeissä
- koko sovellus on ahdettu neljään moduulin: database, functions, gui ja main

------------------------------------
functions moduuli

- sisältää tarkastus funktioita
- jokainen funktio palauttaa joko True, False tai None
- tätä moduulia käytetään database ja gui

------------------------------------
database moduuli

- sisältää databasen luonti ja poisto funktiot
- sisältää kaikki databasen käsittelyyn käytetyt funktiot
- moduuli ei sisällä tarkastuksia
- on pidettävä huoli tämän moduulin funktioita käytettäessä, että annetut arvot ovat HYVÄT

------------------------------------
gui moduuli

- sisältää koko käyttöliittymän
- hyödyntää functions ja database moduulia
- tarkastaa käyttäjän syötteen functions moduulin avulla
- ilmoittaa huonosta syötteestä (syöte huono)
- tekee database muutoksen (syöte hyvä)


(huonosti suunniteltu)
- globaalien muuttujien avulla käsittelee ikkunat ja popups
- ei luokkia, kaikki tehty funktioiden avulla
- ei tapaa testata suoraan eri ikkunoita, joudut main.py kautta menemään aloitus ikkunaan

------------------------------------
main moduuli

- sovelluksen käynnistykseen käytetty moduuli

------------------------------------
Tietokanta (kehno suunnittelu)

- sqlite3 tietokanta
- käyttää 4 eri taulua

(taulut)
- Users
   *   id INTEGER PRIMARY KEY
   *   username TEXT
   *   password TEXT (hashed)
   *   role INTEGER (0=admin, 1=teacher, 2=student, 3=guest)
   *   visible BOOLEAN

- Courses
   *   id INTEGER PRIMARY KEY
   *   tag TEXT
   *   name TEXT
   *   credits INTEGER
   *   open BOOLEAN
   *   visible BOOLEAN

- StudentRoleRequests
   *   id INTEGER PRIMARY KEY
   *   username TEXT
   *   message TEXT
   *   datetime DATETIME

- InCourse
   *   course_id INTEGER REFERENCES Courses
   *   course_tag TEXT REFERENCES Courses
   *   course_name TEXT REFERENCES Courses
   *   course_credits INTEGER REFERENCES Courses
   *   user_id INTEGER REFENCES Users
   *   username TEXT REFERENCES Users
   *   user_role INTEGER REFERENCES Users
   *   grade INTEGER


------------------------------------
Parannettavaa

- gui tulisi muuttaa folderiksi joka koostuu tiedostoista eri käyttäjille siis guest.py, student.py...
- gui olisi hyvä myös vähentää copypastea, ikkunan päivitystä varten käytetään funktioita jotka kopioivat edellisen ikkunan
- tietokannan tauluista voisi tehdä hieman järkevämmät