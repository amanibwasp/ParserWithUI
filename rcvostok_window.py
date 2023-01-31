from PyQt5.QtCore import QEventLoop, QTimer
import openpyxl
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from read_xlsx import read_xlsx
from get_history import get_history
from galamart_parser import parser

class RC_Window(QMainWindow):
    def __init__(self, stack):
        super(RC_Window, self).__init__()
        loadUi('rcvostok.ui', self)
        self.stack = stack
        self.UI()

    def UI(self):
        self.progress_bar.hide()
        self.button_choose_vendors.clicked.connect(self.choose_vendors_path)
        self.button_choose_download.clicked.connect(self.choose_download_path)
        self.button_start.clicked.connect(self.start_parser)
        self.choose_parser_cb.currentIndexChanged.connect(self.toggle_window)

    def toggle_window(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)

    def choose_vendors_path(self):
        self.file_path_vendors = QFileDialog.getOpenFileName()[0]
        self.line_edit_vendors.setText(self.file_path_vendors)

    def choose_download_path(self):
        self.file_path_download = QFileDialog.getExistingDirectory()
        self.line_edit_download.setText(self.file_path_download)

    def start_parser(self):
        self.vendor_codes = read_xlsx(self.line_edit_vendors.text())
        self.directory_of_download = self.line_edit_download.text()
        self.directory_of_download_error = True
        self.vendor_codes_error = True
        if self.vendor_codes == 'empty':
            self.label_vendors.setText('Это обязательное поле')
            self.label_vendors.setStyleSheet('background-color: #aa0000;')
            self.label_vendors.resize(183, 31)
            self.vendor_codes_error = False
        elif self.vendor_codes == 'not xlsx':
            self.label_vendors.setText('Расширение файла должно быть xlsx')
            self.label_vendors.setStyleSheet('background-color: #aa0000;')
            self.label_vendors.resize(290, 31)
            self.vendor_codes_error = False
        else:
            self.label_vendors.setText('Путь к файлу xlsx с артикулами:')
            self.label_vendors.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white;')
            self.label_vendors.resize(251, 31)

        if self.directory_of_download == '':
            self.label_download.setText('Это обязательное поле')
            self.label_download.setStyleSheet('background-color: #aa0000;')
            self.label_download.resize(183, 31)
            self.directory_of_download_error = False
        else:
            self.label_download.setText('Директория, куда будут скачаны файлы парсинга:')
            self.label_download.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: white;')
            self.label_download.resize(381, 31)
        if self.directory_of_download_error and self.vendor_codes_error:
            self.button_choose_vendors.hide()
            self.button_choose_download.hide()
            self.button_start.hide()
            self.vendor_codes_count = len(self.vendor_codes)
            self.done_count = 0
            self.progress_bar.show()
            self.vendor_codes = [v.strip() for v in self.vendor_codes]
            self.create_excel()
            for vendor_code in self.vendor_codes:
                parser_response = parser(vendor_code, self.params_dict_pattern())
                if parser_response == 'Error': continue
                self.update_excel(parser_response[0], parser_response[1])
                self.change_progress_bar()
                loop = QEventLoop()
                QTimer.singleShot(2000, loop.quit)
                loop.exec_()
            history = get_history()
            self.wb_params.save(f'{self.directory_of_download}/Параметры {history}.xlsx')
            self.wb_imgs.save(f'{self.directory_of_download}/Изображения {history}.xlsx')
            self.progress_bar.hide()
            self.button_choose_vendors.show()
            self.button_choose_download.show()
            self.button_start.show()

    def change_progress_bar(self):
        self.done_count += 1
        progress = int(self.done_count * 100 / self.vendor_codes_count)
        self.progress_bar.setValue(progress)

    def params_dict_pattern(self):
        params_dict = {
            'Цвет': 'Не указан',
            'Бренд': 'Не указан',
            'Название': 'Не указано',
            'Артикул продавца': 'Не указан',
            'Состав': 'Не указан',
            'Описание': 'Не указано',
            'Вес': 'Не указан',
            'Вес в упаковке': 'Не указан',
            'Высота упаковки': 'Не указана',
            'Длина упаковки': 'Не указана',
            'Ширина упаковки': 'Не указана',
            'Страна производства': 'Не указана'
        }
        return params_dict

    def create_excel(self):
        self.wb_params = openpyxl.Workbook()
        self.wh_params = self.wb_params.active
        self.wh_params.title = 'Параметры'
        self.wh_params.append(list(self.params_dict_pattern().keys()))

        self.wb_imgs = openpyxl.Workbook()
        self.wh_imgs = self.wb_imgs.active
        self.wh_imgs.title = 'Изображения'
        self.wh_imgs.append(['Артикул продавца', 'Медиафайлы'])

    def update_excel(self, params_dict, images_hrefs):
        self.wh_params.append(list(params_dict.values()))
        self.wh_imgs.append([params_dict['Артикул продавца'], ';'.join(images_hrefs)])
