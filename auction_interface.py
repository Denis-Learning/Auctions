# - * - coding: utf8 -*-
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer,QDateTime
from PyQt5.QtGui import QPixmap
import sys
import time
from auction_funcion import User, Trading
import os

# у нас много участников которые торгуются за часы в онлайн режиме. Есть ограничиние в 30мин. Есть определенный шаг. Если в последную минуту кто-о делает ставку то аукцион продлевается на минуту и так до бесконечности. Вывод результатов аукциона.

class Interface(QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()  # просто обязательный код, объединяет init'ы
        self.resize(800, 500)  # размеры окна программы
        self.setWindowTitle('Авторизация')
        self.user = User()

        self.login_lable = QtWidgets.QLabel(self)  # текстовое поле для ввода рефа
        self.login_lable.setGeometry(QtCore.QRect(95, 50, 40, 20)) # ВАЖНО первые две координаты - это левый верхний угол окна, а последние две его размеры
        self.login_lable.setText('логин')
        self.login_edit = QtWidgets.QLineEdit(self)  # текстовое поле для ввода бренда
        self.login_edit.setGeometry(QtCore.QRect(150, 50, 400, 20))  # задаем габариты окна ввода бренда

        self.pass_lable = QtWidgets.QLabel(self)  # QLabel - значит некликабельное окно
        self.pass_lable.setGeometry(QtCore.QRect(95, 80, 40, 20))
        self.pass_lable.setText('пароль')
        self.pass_edit = QtWidgets.QLineEdit(self)  # текстовое поле для ввода рефа
        self.pass_edit.setGeometry(QtCore.QRect(150, 80, 400, 20))  # задаем габариты окна ввода рефа

        self.ok_button = QtWidgets.QPushButton(self)  # создаем кнопку без координат
        self.ok_button.setGeometry(QtCore.QRect(300, 120, 100, 50))  # габариты кнопки
        self.ok_button.setText('войти')  # присваиваем название кнопке
        self.ok_button.clicked.connect(self.authorization)

    def authorization(self):
        self.user.login = self.login_edit.text()
        self.user.password = self.pass_edit.text()
        self.user.authorization_func()
        if self.user.authorization_func():  # если авторизация прошла успешно, то закрываем старое окно и открываем новое
            # self.auct = Auction(self.user)  # нужен self чтобы метод работал постоянно,,, Auction(self.user) - нужен чтобы передать логин в следующее окно Auction
            # self.auct.show()
            # self.close()  # закрытие старого, важно закрытие и открытие писать в этом классе!
            self.select_w = Select_watch(self.user)
            self.select_w.show()
            self.close()


class Select_watch(QMainWindow):
    def __init__(self, user):
        super(Select_watch, self).__init__()  # просто обязательный код, объединяет init'ы
        self.resize(650, 400)  # размеры окна программы
        self.setWindowTitle('Выбор часов')
        self.user = user

        self.list_watch_lable = QtWidgets.QLabel(self)
        self.list_watch_lable.setGeometry(QtCore.QRect(10, 10, 350, 80))
        self.list_watch_lable.setText('Выберите часы')

        self.list_watch = QtWidgets.QLabel(self)
        self.list_watch.setGeometry(QtCore.QRect(95, 150, 550, 80))
        file = open('watch_par.txt', 'r', encoding='windows-1251').readlines()
        self.list_watch_lable.setText('\n'.join(file))

        self.select_button_lable = QtWidgets.QLabel(self)
        self.select_button_lable.setGeometry(QtCore.QRect(30, 80, 145, 50))
        self.select_button_lable.setText('Введите номер часов')

        self.watch_number = QtWidgets.QLineEdit(self)  # текстовое поле для ввода бренда
        self.watch_number.setGeometry(QtCore.QRect(160, 90, 24, 24))

        self.select_button = QtWidgets.QPushButton(self)
        self.select_button.setGeometry(QtCore.QRect(190, 90, 40, 25))  # габариты кнопки
        self.select_button.setText('ок')  # присваиваем название кнопке
        self.select_button.clicked.connect(self.create_auction)

    # метод который сначала проверяет идет ли аукцион (в файле opened auctions), если нет то создать новый
    def create_auction(self):
        def find(name, path):  # метод который принимает имя файла и путь к папке и возвращает путь к этому файлу в папке
            for root, dirs, files in os.walk(path):
                if name in files:
                    return os.path.join(root)  # path - путь до папки, а root - путь к файлу в этой папке

        file = open('watch_par.txt', 'r', encoding='windows-1251').readlines()
        d = eval(file[(int(self.watch_number.text()) - 1)])  # eval чтобы превратить набор строк в словарь!
        print(type(d))
        if find((d['brand'] + d['ref'] + '.txt').replace(' ', ''), 'C:\\Users\\Denis\\PycharmProjects\\auction'):  # на другом компе другой путь!!! НЕ забыть это поменять!!!!!!!!!!!!!!!!!!!!!
            self.auct_file = open((d['brand'] + d['ref'] + '.txt').replace(' ', ''), 'a', encoding='windows-1251')  # если файл с аукционом найден то мы присваиваем переменной self.auct_file этот файл в режиме дописывания 'a'
            print('a')
        else:
            self.auct_file = open((d['brand'] + d['ref'] + '.txt').replace(' ', ''), 'w+', encoding='windows-1251')  # если файл с аукционом не найден то мы создаем файл 'w+
            print('w+')

        self.auction_show = Auction(self.user, (d['brand'] + d['ref'] + '.txt').replace(' ', ''), d)  #код который передает инфу и юзере и часах в которые он зашел
        self.auction_show.show()
        self.close()



class Auction(QMainWindow):
    def __init__(self, user, auct_file, d):
        super(Auction, self).__init__()
        self.resize(800, 800)  # размеры окна программы
        self.setWindowTitle('Аукционы')
        self.user = user
        self.auct_file = auct_file
        self.d = d


        self.login_lable_au = QtWidgets.QLabel(self)
        self.login_lable_au.setGeometry(QtCore.QRect(740, 10, 70, 20))
        self.login_lable_au.setText(self.user.login)

        self.description = QtWidgets.QLabel(self)
        self.description.setGeometry(QtCore.QRect(40, 50, 100, 20))
        self.description.setText('<b>Описание лота</b>')

        self.full_description = QtWidgets.QLabel(self)
        self.full_description.setGeometry(QtCore.QRect(40, 90, 450, 30))
        self.full_description.setText(str(self.d))  # если оставить self.d - то это словарь и он не откроется

        self.description = QtWidgets.QLabel(self)
        self.description.setGeometry(QtCore.QRect(40, 150, 140, 20))
        self.description.setText('<b>Процесс торгов</b>')

        self.global_rate_lable = QtWidgets.QLabel(self)
        self.global_rate_lable.setGeometry(QtCore.QRect(40, 200, 120, 20))
        self.global_rate_lable.setText('Текущая ставка')

        self.global_rate = QtWidgets.QLabel(self)
        self.global_rate.setGeometry(QtCore.QRect(170, 200, 60, 20))
        # self.global_rate.setText(str())

        self.login_rate_lable = QtWidgets.QLabel(self)
        self.login_rate_lable.setGeometry(QtCore.QRect(40, 250, 120, 20))
        self.login_rate_lable.setText('Повысить ставку до:')

        self.login_rate = QtWidgets.QLineEdit(self)
        self.login_rate.setGeometry(QtCore.QRect(170, 250, 60, 20))

        self.save_rate_button = QtWidgets.QPushButton(self)
        self.save_rate_button.setGeometry(QtCore.QRect(250, 235, 100, 50))
        self.save_rate_button.setText('Отправить')
        self.save_rate_button.clicked.connect(self.save_rate)
        self.save_rate_button.clicked.connect(self.raise_rate)

        # таймер для автообновления данных по другим пользователям
        self.timer = QTimer()
        self.timer.timeout.connect(self.raise_rate)
        self.timer.start(2)


    def save_rate(self):
        file = open(self.auct_file, 'a+', encoding='windows-1251')
        file.write(','.join([self.login_rate.text(), self.user.login]) + '\n')
        file.close()

    # метод показа текущей ставки и подсказки для повышения
    def raise_rate(self):
        max_rate = int(self.d['start_price'])
        file = open(self.auct_file, 'r', encoding='windows-1251').readlines()
        for line in file:
            if int(line.split(',')[0]) > max_rate:
                max_rate = int(line.split(',')[0])
        self.global_rate.setText(str(max_rate))
        self.login_rate.setText(str(int(max_rate) + int(self.d['step'])))

def start():
    app = QApplication(sys.argv) #обязательная строчка
    win1 = Interface()
    win2 = Interface()
    win1.show() #показать окно
    win2.show() #показать окно
    sys.exit(app.exec_()) #выход из программы

start()


#TODO дописать работу с файлом бренд-реф для приема ставок

