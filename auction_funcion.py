# - * - coding: utf8 -*-

# нужно два скрипта, которые ссылаются на один тексовый файл со ставками

class User:
    def __init__(self):
        self.login = ''
        self.password = ''
        self.file_link = ''

    # метод авторизации
    def authorization_func(self):
        file = open('passwords.txt', 'r', encoding='windows-1251').readlines()
        for line in file:
            if line.split(',')[0] == self.login and line.split(',')[1][:-1] == self.password:  # [:-1] чтобы отрезать enter в конце txt файла
                return True


class Trading:
    def __init__(self):
        self.watch_parameters = {}  # подгружать через json
        self.last_rate = ''
        # self.auct_file =



    def show_description(self):  # показ описания часов
        file = open('watch_par.txt', 'r', encoding='windows-1251').readlines()
        for line in file:
            return line

    def save_login_rate(self, rate, login):  # сохранение ставки от каждого логина
        f = open('rates.txt', 'a+', encoding='windows-1251').readlines()
        # file = open('watch_par.txt', 'r', encoding='windows-1251').readlines()
        # for rate in f:
        #     if rate %
        f.write(','.join([rate, login]) + '\n')
        f.close()  # ставка не может быть сохранена если меньше текущей и если некратна шагу

    # def processing(self):  # обработка ставок, расчет шага ставки, вычисление лидера и добавка времени, вывод всего этого на экран






#TODO добавить добавить проверку на максимальную ставку, и соответсвие шагу, а лучше просто добавить ставку в виде ко-ва шагов. Обновление ставок в реальном времени (или кнопка со ставкой запускала процесс обновления)






# a = User()
# a.login = 'denis'
# a.password = '12345%'
#
# print(a.authorization_func())

# a = Trading()
# print(a.show_description())