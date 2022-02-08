import os
import sys

import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.spn = 0.01
        self.coord_x = 37.530887
        self.coord_y = 55.703118
        self.l_map = 'map'
        self.getImage(self.spn, self.coord_x, self.coord_y, self.l_map)
        self.initUI()

    def getImage(self, spn, coord_x, coord_y, l_map):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord_x}," \
                      f"{coord_y}&spn={spn},{spn}&l={l_map}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('MapAPI')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.scheme = QPushButton('Схема', self)
        self.scheme.setFocusPolicy(Qt.NoFocus)
        self.scheme.clicked.connect(self.checked)
        self.scheme.move(500, 20)

        self.satellite = QPushButton('Спутник', self)
        self.satellite.setFocusPolicy(Qt.NoFocus)
        self.satellite.clicked.connect(self.checked)
        self.satellite.move(500, 70)

        self.hybrid = QPushButton('Гибрид', self)
        self.hybrid.setFocusPolicy(Qt.NoFocus)
        self.hybrid.clicked.connect(self.checked)
        self.hybrid.move(500, 120)

    def checked(self):
        signal = self.sender()
        if signal == self.scheme:
            self.l_map = "map"
            self.run()
        elif signal == self.satellite:
            self.l_map = "sat"
            self.run()
        elif signal == self.hybrid:
            self.l_map = "sat,skl"
            self.run()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp:
            if self.spn < 5.0:
                self.spn += 0.1
                self.run()
        elif key == Qt.Key_PageDown:
            if self.spn > 0.1:
                self.spn -= 0.1
                self.run()
        elif key == Qt.Key_Up:
            if self.coord_y < 84:
                self.coord_y += 0.1
                self.run()
        elif key == Qt.Key_Down:
            if self.coord_y > -84:
                self.coord_y -= 0.1
                self.run()
        elif key == Qt.Key_Right:
            if self.coord_x < 179:
                self.coord_x += 0.1
                self.run()
        elif key == Qt.Key_Left:
            if self.coord_x > -179:
                self.coord_x -= 0.1
                self.run()

    def run(self):
        self.getImage(self.spn, self.coord_x, self.coord_y, self.l_map)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
