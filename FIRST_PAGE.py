import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QWidget
from LOGINS import isornotinclients, set_user_to_db, isornotdoctor, isLogin, isnameindb, setNewName, doctorsname
from LOGINS import addDescr, updateDiagnoz, deleteFromDb, deleteDiagnozFromDb, islgnmindocs, addDiagnoz, set_to_doctor_db
import time
import sqlite3
from PyQt5 import QtCore, QtMultimedia


class MainW(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('the_first_page.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Система')
        self.signin.clicked.connect(self.signinn)
        self.signup.clicked.connect(self.signupp)
        self.tableofdocs.clicked.connect(self.tableDocs)

        self.count = 1
        self.load_mp3('Dreaming.mp3')
        self.volume.clicked.connect(self.value_change)

        self.show()

    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.play()

    def value_change(self):
        if self.count == 0:
            self.player.play()
            self.count = 1
        else:
            self.player.pause()
            self.count = 0

    def signupp(self):
        self.third_form = Logup(self, "Данные для формы")
        self.third_form.show()

    def signinn(self):
        self.second_form = Login(self, "Данные для формы")
        self.second_form.show()

    def tableDocs(self):
        self.docs_form = Main_docs(self, "Данные для формы")
        self.docs_form.show()


class Logup(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('registration.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(800, 300, 300, 350)
        self.setWindowTitle('Регистрация')
        self.pushButton.clicked.connect(self.goto)

    def goto(self):
        if self.name.text() == '' or self.name_2.text() == '':
            self.label_3.setText('Заполните все поля')
        elif isornotinclients(self.name.text(), self.name_2.text()):
            self.label_3.setText('Такой пользователь существует\nВойдите или выберите другой логин')
        elif isLogin(self.name.text()) and not isornotinclients(self.name.text(), self.name_2.text()):
            self.label_3.setText('Введите другой логин')
        else:
            set_user_to_db(self.name.text(), self.name_2.text(), '3')
            time.sleep(2)
            self.label_3.setText('Успешно')

            self.form = Profileofpatient(self, self.name.text())
            self.form.show()
            self.close()


class Login(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('login_form.ui', self)
        self.loginu = args[1]
        self.initUI(self.loginu)

    def initUI(self, args):
        self.setWindowTitle('Вход в систему')
        self.push_login.clicked.connect(self.goto)

    def goto(self):
        if self.name_place.text() == '' or self.pswrd.text() == '':
            self.errorrr.setText('Заполните все поля')
        elif self.name_place.text() == 'kseniya_admin' and self.pswrd.text() == 'admin':
            self.errorrr.setText('ADMIN')
            time.sleep(2)
            self.adminPr = Admin_profile(self, self.name_place.text())
            self.adminPr.show()
            self.close()
        elif isornotinclients(self.name_place.text(), self.pswrd.text()):
            self.errorrr.setText('Успешно')
            self.forms = Profileofpatient(self, self.name_place.text())
            time.sleep(2)
            self.forms.show()
            self.close()
        elif isornotdoctor(self.name_place.text(), self.pswrd.text()):
            self.errorrr.setText('Успешно')
            self.forms = Profileofdoctor(self, self.name_place.text())
            time.sleep(2)
            self.forms.show()
            self.close()
        else:
            self.errorrr.setText('Пользователя\nне существует')


class Users(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi(args[0], self)
        self.ulogin = args[1]
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle(args[2])


class Profileofpatient(Users):
    def __init__(self, *args):
        super().__init__('profile_patient.ui', args[1], 'Profile')

    def initUI(self, args):
        self.nameandfemale.setText(self.ulogin)
        self.visit.clicked.connect(self.docs_visit)
        self.tbl()
        self.up.clicked.connect(self.tbl)

    def tbl(self):
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        d = cur.execute("SELECT date, problem, diagnoz, namemaindoctor, \
        loginmaindoctor FROM diagnoses WHERE login=" + f"'{self.ulogin}'")
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(d):
            row = list(row)
            row.append('0')
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()
        con.commit()
        con.close()

    def docs_visit(self):
        if self.dlogin.text() == '' or self.dname.text() == '' or self.cproblem.text() == '':
            self.errors.setText('Заполните\n все поля')
        elif not islgnmindocs(self.dlogin.text(), self.dname.text()):
            self.errors.setText('Неверный логин\nили имя')
        else:
            addDiagnoz(self.date.text(), self.ulogin, self.dlogin.text(), self.dname.text(), self.cproblem.text())
            self.errors.setText('Отправлено\nТеперь обновите\nВкладку\n"диагнозы"')


class Profileofdoctor(Users):
    def __init__(self, *args):
        super().__init__('profile_doctor.ui', args[1], 'Profile')

    def initUI(self, args):
        self.nameandfemale.setText(doctorsname(self.ulogin))
        self.createNewName.clicked.connect(self.changeName)
        self.fio.clicked.connect(self.setName)
        self.apdate_descr.clicked.connect(self.addDescr)
        self.tabl()
        self.save.clicked.connect(self.save_results)

    def changeName(self):
        self.fio.move(180, 40)
        self.name_space.move(20, 40)
        self.createNewName.move(1000, 80)

    def setName(self):
        self.fio.move(1000, 140)
        self.name_space.move(1000, 40)
        if self.name_space.text() != '':
            self.nameandfemale.setText(self.name_space.text())
            setNewName(self.ulogin, self.name_space.text())
        self.createNewName.move(170, 210)

    def addDescr(self):
        addDescr(self.ulogin, self.descrip.toPlainText())
        time.sleep(1)
        self.complete.setText('Опубликовано')

    def tabl(self):
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        m = cur.execute("SELECT date, login, problem, diagnoz, namemaindoctor FROM diagnoses WHERE loginmaindoctor="
                        + f"'{self.ulogin}'")
        self.tableW.setRowCount(0)
        for i, row in enumerate(m):
            row = list(row)
            row.append('0')
            self.tableW.setRowCount(self.tableW.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableW.setItem(i, j, QTableWidgetItem(elem))
        self.tableW.resizeColumnsToContents()
        con.commit()
        con.close()
        self.show()

    def save_results(self):
        rs = self.tableW.rowCount()
        cs = self.tableW.columnCount()
        a = []
        print(self.ulogin)
        for i in range(rs):
            d = []
            for j in range(cs):
                d.append(self.tableW.item(i, j).text())
            a.append(d)
            updateDiagnoz(d[0], d[1], self.ulogin, d[4], d[2], d[3])
        self.tabl()


class Admin_profile(Users):
    def __init__(self, *args):
        super().__init__('admin.ui', args[1], 'ADMIN')

    def initUI(self, args):
        self.admin_name.setText(self.ulogin)
        self.patientTables()
        self.doctorsTables()
        self.diagnosesTables()
        self.persTables()
        self.pat_del.clicked.connect(self.deletePatient)
        self.doc_del.clicked.connect(self.deleteDoctor)
        self.diag_del.clicked.connect(self.deleteDiagnoz)
        self.add_doctor.clicked.connect(self.insDoc)
        self.restart.clicked.connect(self.doctorsTables)

    def insDoc(self):
        self.ins_form = InsertDoctor(self, "Данные для формы")
        self.ins_form.show()

    def patientTables(self):
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        patients_ = cur.execute("SELECT login, password FROM login_password WHERE who = '3'").fetchall()
        self.patient_table.setRowCount(0)
        for i, row in enumerate(patients_):
            row = list(row)
            row.append('0')
            self.patient_table.setRowCount(self.patient_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.patient_table.setItem(i, j, QTableWidgetItem(elem))
        self.patient_table.resizeColumnsToContents()
        con.commit()
        con.close()

    def doctorsTables(self):
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        dct = cur.execute("SELECT login, description, name FROM doctors").fetchall()
        self.docs_table.setRowCount(0)
        for i, row in enumerate(dct):
            row = list(row)
            row.append('0')
            self.docs_table.setRowCount(self.docs_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.docs_table.setItem(i, j, QTableWidgetItem(elem))
        self.docs_table.resizeColumnsToContents()
        con.commit()
        con.close()

    def diagnosesTables(self):
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        diz = cur.execute("SELECT date, login, loginmaindoctor, "
                          "namemaindoctor, problem, diagnoz FROM diagnoses").fetchall()
        self.diagz_table.setRowCount(0)
        for i, row in enumerate(diz):
            row = list(row)
            row.append('0')
            self.diagz_table.setRowCount(self.diagz_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.diagz_table.setItem(i, j, QTableWidgetItem(elem))
        self.diagz_table.resizeColumnsToContents()
        con.commit()
        con.close()

    def persTables(self):
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        who = cur.execute(
            "SELECT id, person FROM personality").fetchall()
        self.who_table.setRowCount(0)
        for i, row in enumerate(who):
            row = list(row)
            row.append('0')
            self.who_table.setRowCount(self.who_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.who_table.setItem(i, j, QTableWidgetItem(elem))
        self.who_table.resizeColumnsToContents()
        con.commit()
        con.close()

    def deletePatient(self):
        deleteFromDb('login_password', 'login', self.patient_table.item(self.patient_table.currentRow(), 0).text())
        self.patientTables()

    def deleteDoctor(self):
        deleteFromDb('doctors', 'login', self.docs_table.item(self.docs_table.currentRow(), 0).text())
        deleteFromDb('login_password', 'login', self.docs_table.item(self.docs_table.currentRow(), 0).text())
        self.doctorsTables()

    def deleteDiagnoz(self):
        deleteDiagnozFromDb(self.diagz_table.item(self.diagz_table.currentRow(), 0).text(),
                            self.diagz_table.item(self.diagz_table.currentRow(), 1).text(),
                            self.diagz_table.item(self.diagz_table.currentRow(), 2).text(),
                            self.diagz_table.item(self.diagz_table.currentRow(), 3).text(),
                            self.diagz_table.item(self.diagz_table.currentRow(), 4).text(),
                            self.diagz_table.item(self.diagz_table.currentRow(), 5).text())
        self.diagnosesTables()


class InsertDoctor(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('add_person.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Регистрация врача')
        self.reg.clicked.connect(self.registrationOfDoctor)

    def registrationOfDoctor(self):
        if self.login_.text() == '' or self.password_.text() == '':
            self.errors_.setText('Заполните все поля')
        elif isornotdoctor(self.login_.text(), self.password_.text()):
            self.errors_.setText('Такой пользователь существует\nВойдите или выберите другой логин')
        elif isLogin(self.login_.text()) and not isornotdoctor(self.login_.text(), self.password_.text()):
            self.errors_.setText('Введите другой логин')
        else:
            set_user_to_db(self.login_.text(), self.password_.text(), '2')
            set_to_doctor_db(self.login_.text(), self.login_.text(), self.descr_.toPlainText())
            time.sleep(2)
            self.errors_.setText('Успешно')


class Main_docs(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('tableofdoctors.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Список докторов')
        con = sqlite3.connect('lowuse.db')
        cur = con.cursor()
        dctrs = cur.execute("SELECT name, login, description FROM doctors").fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(dctrs):
            row = list(row)
            row.append('0')
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()
        con.commit()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainW()
    ex.show()
    sys.exit(app.exec())
