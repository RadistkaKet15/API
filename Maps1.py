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
        self.getImage(self.spn)
        self.initUI()

    def getImage(self, spn):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll=37.530887," \
                      f"55.703118&spn={spn},{spn}&l=map"
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

    def closeEvent(self, event):
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            if self.spn < 5.0:
                self.spn += 0.1
                self.getImage(self.spn)
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
        elif key == Qt.Key_Down:
            if self.spn > 0.1:
                self.spn -= 0.1
                self.getImage(self.spn)
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
