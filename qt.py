# Подключение библиотек
import sys
import sqlite3
# Библиотеки PyQt5
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem
# Окно входа
class Login_window(QMainWindow):
    # Функция иницилизации
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('login_window.ui', self)
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Удаление "Заголовка окна"
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Расширение окна до полноэкранного режима
        self.showMaximized()
        # Добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # Подключение кнопок к функциям
        self.exit_button.clicked.connect(self.exit)
        self.login_button.clicked.connect(self.gateway)
        self.registration_button.clicked.connect(self.registration)
        self.old_pos = None

# Конец блока

    # Закрыть приложение
    def exit(self):
        self.close()

    # Вход в систему
    def gateway(self):
        # Список логинов
        result_1 = basa_cursor.execute('''SELECT login FROM People''').fetchall()
        spis_with_login = []
        for i in result_1:
            spis_with_login.append(i[0])
        # Проверка на существование логина и корректнось пароля
        if self.login.text() in spis_with_login:
            peop = basa_cursor.execute('''SELECT * FROM People WHERE login = (?)''', (self.login.text(),)).fetchall()[0]
            if peop[3] == self.password.text():
                #main_window.set_id_gateway(peop[0])
                # Сохранение id пользователя
                id_gateway = open('id_gateway.txt', 'w+')
                id_gateway.write(str(peop[0]))
                # Открытие окна меню
                res = self.basa_cursor.execute('''SELECT id FROM People WHERE login=(?)''', (self.login.text(),)).fetchall()[-1][0]
                main_window.set_id(res)
                main_window.set_name(peop[1])
                main_window.show()
                self.close()
            else:
                # Ошибка
                self.error.setText('Неверный логин или пароль.')
        else:
            # Ошибка
            self.error.setText('Неверный логин или пароль.')

    # Регистрация в систему
    def registration(self):
        registration_window.show()
        self.close()


class Registration_window(QMainWindow):
    def __init__(self, basa_d):
        super().__init__()
        # Подключение дизайна
        uic.loadUi('registration_window.ui', self)
        # Расширение окна до полноэкранного режима
        self.showMaximized()
        # Удаление "Заголовка" приложения
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # добавление иконки
        self.setWindowIcon(QtGui.QIcon('icon_2.png'))
        # База данных
        self.basa_d = basa_d
        self.basa_cursor = basa_d.cursor()
        self.basa_d.commit()
        # Подключение кнопок
        self.registration_button.clicked.connect(self.check)
        self.exit_button.clicked.connect(self.exit)
        self.old_pos = None

    # Функция проверки и добавления в базу данных
    def check(self):
        # Получение информации из окна
        name = str(self.name.text())
        login = str(self.login.text())
        password_1 = str(self.password.text())
        password_2 = str(self.password_2.text())
        in_text = True
        # Получение всех логинов, во избежания повторения
        res_l = self.basa_cursor.execute('''SELECT login FROM People''').fetchall()
        logins = []
        for i in res_l:
            logins.append(i[0])
        # Проверка на содержания полей
        text = 'qwertyuiopasdfghjklzxcvbnm йцукенгшщзхъэждлорпавыфячсмитьбю_QWERTYUIOPLKJHGFDSAZXCVBNM ЙЦУКЕНГШЩЗХЪЭЖДЛОРПАВЫФЯЧСМИТЬБЮ 1234567890'
        t_1 = '@.'
        for i in name:
            if i not in text:
                in_text = False
        for i in login:
            if (i not in text) and (i not in t_1):
                in_text = False
        for i in password_1:
            if i not in text:
                in_text = False
        is_check = True
        # Проверка на корректность длинны
        if ((len(name) <= 3) or (len(name) >= 51)) or ((len(password_1) <= 3) or (len(password_1) >= 51)) or ((len(login) <= 3) or (len(login) >= 51)) or ((len(password_2) <= 3) or (len(password_2) >= 51)) :
            self.error.setText('Длинна введённых данных должна быть от 4 до 50 символов.')
            is_check = False
        # Проверка на корректность символов
        elif not in_text:
            self.error.setText('Вы можете использовать только цифры, символы латиницы и кирилицы.')
            is_check = False
        # Проверка на незанятость логина
        elif login in logins:
            self.error.setText('Этот логин уже зарегистрирован.')
            is_check = False
        # Проверка на верное повторение пароля
        elif password_1 != password_2:
            self.error.setText('Пароли не совпадают.')
            is_check = False
        # Добавление в базу данных
        if is_check:
            print(10)
            self.basa_cursor.execute('''INSERT INTO People (name, login, password) VALUES (?, ?, ?)''', (name, login, password_1))
            self.basa_d.commit()
            res = self.basa_cursor.execute('''SELECT * FROM People WHERE login=(?)''', (login,)).fetchall()[-1][0]
            print(12)
            main_window.set_id(res)
            main_window.set_name(name)
            print(14)
            main_window.show()
            self.close()

    # Закрыть приложение
    def exit(self):
        self.close()
