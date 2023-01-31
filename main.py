from PyQt5.QtWidgets import QApplication, QStackedWidget
from login_window import Login
from galamart_window import G_Window
from rcvostok_window import RC_Window
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stack = QStackedWidget()
    login_window = Login(stack)
    galamart_window = G_Window(stack)
    rcvostok_window = RC_Window(stack)
    stack.addWidget(login_window)
    stack.addWidget(galamart_window)
    stack.addWidget(rcvostok_window)
    stack.setWindowTitle('Авторизация')
    stack.setFixedWidth(480)
    stack.setFixedHeight(600)
    stack.show()
    sys.exit(app.exec_())