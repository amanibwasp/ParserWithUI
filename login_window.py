from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from config import password, login


class Login(QDialog):
    def __init__(self, stack):
        super(Login, self).__init__()
        loadUi('login.ui', self)
        self.stack = stack
        self.UI()

    def UI(self):
        self.login_button.clicked.connect(self.login)

    def login(self):
        login_text = self.line_edit_login.text()
        password_text = self.line_edit_password.text()
        if login_text == login and password_text == password:
            self.stack.setWindowTitle('Парсер')
            self.stack.setCurrentIndex(self.stack.currentIndex() + 1)
            self.stack.setFixedWidth(700)
        else:
            self.login_main_label.setText('Неправильный логин или пароль')
