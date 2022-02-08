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
        self.format_map = "png"
        self.geocode = 'Москва'
        self.geocode_x = 0
        self.geocode_y = 0
        self.metka = 0
        self.getImage(self.spn, self.coord_x, self.coord_y, self.l_map,
                      self.geocode_x, self.geocode_y)

        self.setMouseTracking(True)

        self.initUI()

    def getImage(self, spn, coord_x, coord_y, l_map, geocode_x, geocode_y):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coord_x}," \
                      f"{coord_y}&spn={spn},{spn}&l={l_map}&pt={geocode_x},{geocode_y},flag"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = f"map.{self.format_map}"
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

        self.line = QLineEdit(self)
        self.line.setFocusPolicy(Qt.ClickFocus)
        self.line.move(20, 20)

        self.find_it = QPushButton('Искать', self)
        self.find_it.setFocusPolicy(Qt.NoFocus)
        self.find_it.clicked.connect(self.find_it_func)
        self.find_it.move(20, 50)

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def find_it_func(self):
        self.line.setEnabled(False)
        self.line.setEnabled(True)
        try:
            self.geocode = self.line.text()
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": self.geocode,
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"].split()
            self.geocode_x = self.coord_x = float(toponym_coodrinates[0])
            self.geocode_y = self.coord_y = float(toponym_coodrinates[1])
            print(self.coord_x, self.coord_y)
            self.run()
        except Exception:
            print('WTF bro?!')

    def checked(self):
        signal = self.sender()
        if signal == self.scheme:
            self.l_map = "map"
            self.format_map = "png"
            self.run()
        elif signal == self.satellite:
            self.l_map = "sat"
            self.format_map = "png"
            self.run()
        elif signal == self.hybrid:
            self.l_map = "sat,skl"
            self.format_map = "png"
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
        self.getImage(self.spn, self.coord_x, self.coord_y, self.l_map,
                      self.geocode_x, self.geocode_y)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
