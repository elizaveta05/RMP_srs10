from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd

# Класс для вызова функции всплывающего окна
class PopupWindow(Widget):
    def btn(self):
        popFun()

# Класс для создания GUI всплывающего окна
class P(FloatLayout):
    pass

# Функция для отображения содержимого всплывающего окна
def popFun():
    show = P()
    window = Popup(title="popup", content=show, size_hint=(None, None), size=(300, 300))
    window.open()

# Класс для приема информации пользователя и валидации
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):
        # Проверка наличия электронной почты в базе данных
        if self.email.text not in users['Email'].unique():
            popFun()
        else:
            # Переключение экрана для отображения результата валидации
            sm.current = 'logdata'
            # Сброс значений полей ввода
            self.email.text = ""
            self.pwd.text = ""

# Класс для регистрации нового пользователя
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):
        # Создание DataFrame с информацией о пользователе
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]], columns=['Name', 'Email', 'Password'])
        if self.email.text != "":
            if self.email.text not in users['Email'].unique():
                # Если адрес электронной почты не существует, добавляем в базу данных и переходим на экран входа
                user.to_csv('login.csv', mode='a', header=False, index=False)
                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
        else:
            # Если значения пусты или некорректны, показываем всплывающее окно
            popFun()

# Класс для отображения результата валидации
class logDataWindow(Screen):
    pass

# Класс для управления экранами
class windowManager(ScreenManager):
    pass

# Загрузка kv-файла
kv = Builder.load_file('login.kv')
sm = windowManager()

# Чтение данных из файла
users = pd.read_csv('login.csv')

# Добавление экранов
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))

# Класс для создания GUI
class loginMain(App):
    def build(self):
        return sm

# Основная функция
if __name__ == "__main__":
    loginMain().run()