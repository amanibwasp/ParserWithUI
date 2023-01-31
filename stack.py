from PyQt5.QtWidgets import QStackedWidget, QComboBox


class Stack(QStackedWidget):
    def create_stack(self, windows: list):
        for window in windows:
            self.addWidget(window)
        self.setWindowTitle('Авторизация')
        self.setFixedWidth(480)
        self.setFixedHeight(600)
        self.show()

    def toggle_window(self, cb: QComboBox):
        if cb.currentText() == 'RcVostok':
            self.setWindowTitle('RcVostok')
            self.setCurrentIndex(self.currentIndex() + 1)
            self.setFixedWidth(700)
        elif cb.currentText() == 'Galamart':
            self.setWindowTitle('Galamart')
            self.setCurrentIndex(self.currentIndex() - 1)
            self.setFixedWidth(700)


s = Stack()
