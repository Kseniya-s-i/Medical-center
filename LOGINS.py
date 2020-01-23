import sqlite3


def isLogin(lgn):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    s = cur.execute("SELECT login FROM login_password").fetchall()
    for el in s:
        if el[0] == lgn:
            return True
    return False


def isornotinclients(lgn, pswrd):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    s = cur.execute("SELECT login, password, who FROM login_password").fetchall()
    for el in s:
        if el[0] == lgn and el[1] == pswrd and el[2] == 3:
            con.commit()
            con.close()
            return True
    con.commit()
    con.close()
    return False


def isornotdoctor(lgn, pswrd):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    s = cur.execute("SELECT login, password, who FROM login_password").fetchall()
    for el in s:
        if el[0] == lgn and el[1] == pswrd and el[2] == 2:
            con.commit()
            con.close()
            return True
    con.commit()
    con.close()
    return False


def set_to_doctor_db(login, name, des):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    m = cur.execute("INSERT INTO doctors(login, who, description, name) VALUES(" + f"'{login}', '2', '{des}', '{name}')")
    con.commit()
    con.close()


def islgnmindocs(lgn, name):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    names = cur.execute("SELECT login, name FROM doctors").fetchall()
    for el in names:
        if el[0] == lgn and el[1] == name:
            return True
    con.commit()
    con.close()
    return False

def isnameindb(login, name):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    names = cur.execute("SELECT login, name FROM doctors WHERE login =" + f"'{login}'").fetchall()
    if names[1] == '':
        return False
    con.commit()
    con.close()
    return True


def doctorsname(lgn):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    names = cur.execute("SELECT name FROM doctors WHERE login =" + f"'{lgn}'").fetchone()
    con.commit()
    con.close()
    return names[0]


def setNewName(login, name):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    m = cur.execute("UPDATE doctors SET name = " + f"'{name}'" + " WHERE login=" + f"'{login}'")
    con.commit()
    con.close()


def set_user_to_db(lgn, pswrd, w):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    s = cur.execute("INSERT INTO login_password(login, password, who) VALUES(" + f"'{lgn}', '{pswrd}', '{w}')")
    con.commit()
    con.close()


def addDescr(login, decsr):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    m = cur.execute("UPDATE doctors SET description = " + f"'{decsr}'" + " WHERE login=" + f"'{login}'")
    con.commit()
    con.close()


def addDiagnoz(date, login, lgmaindoc, namemaindc, problem):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    d = cur.execute("INSERT INTO diagnoses(date, login, loginmaindoctor, namemaindoctor, \
    problem, diagnoz) VALUES(" + f"'{date}', '{login}', '{lgmaindoc}', '{namemaindc}', '{problem}', '')")
    con.commit()
    con.close()

def updateDiagnoz(date, login, lgmndc, nmmndc, problem, diagnoz):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    d = cur.execute("UPDATE diagnoses SET diagnoz = " + f"'{diagnoz}' " + "WHERE date = " + f"'{date}' " + "AND login = "
                    + f"'{login}' " + "AND loginmaindoctor = " + f"'{lgmndc}' " + "AND namemaindoctor = " + f"'{nmmndc}' "
                    + "AND problem = " + f"'{problem}'")
    con.commit()
    con.close()

def deleteFromDb(namedb, current_parametr, param_value):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    f = cur.execute("DELETE FROM " + f"{namedb} " + f"WHERE " + f"{current_parametr} = " + f"'{param_value}'")
    con.commit()
    con.close()

def deleteDiagnozFromDb(date, login, lgmndc, nmmndc, problem, diagnoz):
    con = sqlite3.connect('lowuse.db')
    cur = con.cursor()
    h = cur.execute("DELETE FROM diagnoses WHERE date = " + f"'{date}' " + f"AND login = " + f"'{login}' " +\
                    f"AND loginmaindoctor = " + f"'{lgmndc}' " + f"AND namemaindoctor = " + f"'{nmmndc}' " +\
                    f"AND problem = " + f"'{problem}' " + f"AND diagnoz = " + f"'{diagnoz}'")
    con.commit()
    con.close()
