import sys

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton, QRadioButton
import requests


class MainWindow(QMainWindow):
    g_map: QLabel
    g_search: QLineEdit
    g_layer1: QPushButton
    g_layer2: QPushButton
    g_layer3: QPushButton
    lightButton: QRadioButton
    darkButton: QRadioButton
    press_delta = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)

        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.map_key = ''
        self.set_theme = 'light'

        self.lightButton.clicked.connect(self.set_theme_light)
        self.darkButton.clicked.connect(self.set_theme_dark)

        self.refresh_map()

    def set_theme_light(self):
        self.set_theme = 'light'
        self.refresh_map()

    def set_theme_dark(self):
        self.set_theme = 'dark'
        self.refresh_map()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
        if key == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if key == Qt.Key.Key_Left:
            self.map_ll[0] -= self.press_delta
        if key == Qt.Key.Key_Right:
            self.map_ll[0] += self.press_delta
        if key == Qt.Key.Key_Up:
            self.map_ll[1] += self.press_delta
        if key == Qt.Key.Key_Down:
            self.map_ll[1] -= self.press_delta

        if key == Qt.Key.Key_D:
            self.set_theme = 'dark'
        if key == Qt.Key.Key_L:
            self.set_theme = 'light'

        elif key == Qt.Key.Key_Escape:
            self.g_map.setFocus()

        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": f'{self.map_ll[0]},{self.map_ll[1]}',
            "maptype": self.map_l,
            "z": self.map_zoom,
            "theme": self.set_theme,
            "apikey": '3e71b5f1-04ae-4416-832f-245df696c138'
        }
        response = requests.get('https://static-maps.yandex.ru/v1', params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.g_map.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
