import sys
import threading
from random import choice
from time import sleep

from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.htools import RoomFurni
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from exalemao_gui import Ui_Exalemao


class Exalemao:
    def __init__(
        self,
        ext: Extension,
        floorheightmap="FloorHeightMap",
        notificationdialog="NotificationDialog",
        roomready="RoomReady",
    ):
        self.__ext = ext
        self.floorheightmap = floorheightmap

        self.tiles = []
        self.furnis = {"floor": [], "wall": []}

        self.toggled = False

        room_furni = RoomFurni(ext)
        room_furni.on_floor_furni_load(self.on_floor_furni_load)
        room_furni.on_wall_furni_load(self.on_wall_furni_load)

        ext.intercept(Direction.TO_CLIENT,
                      self.on_floor_height_map, floorheightmap)
        ext.intercept(Direction.TO_CLIENT, self.on_room_ready, roomready)

        ext.intercept(
            Direction.TO_CLIENT,
            self.on_alerts,
            notificationdialog,
            mode="async_modify",
        )

        self.initialize_gui()

    def initialize_gui(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = Ui_Exalemao()
        self.ui.setupUi(self.window)

        self.ui.start.clicked.connect(self.on_start)
        self.ui.move_furni.clicked.connect(
            lambda: self.can_stop(self.ui.move_furni))
        self.ui.move_wall.clicked.connect(
            lambda: self.can_stop(self.ui.move_wall))

        self.window.show()
        sys.exit(self.app.exec_())

    def on_start(self):
        if self.can_start():
            alemao = threading.Thread(target=self.alemao_room)
            alemao.start()

    def on_floor_height_map(self, message):
        (_, _) = message.packet.read("iB")

        self.tiles = self.get_tiles(message.packet.read_string())

    def on_floor_furni_load(self, furnis):
        self.furnis["floor"] = [furni.id for furni in furnis]

    def on_wall_furni_load(self, furnis):
        self.furnis["wall"] = [(int(furni.id), furni.location)
                               for furni in furnis]

    def on_alerts(self, message):
        message.is_blocked = True

    def on_room_ready(self, message):
        self.ui.room_loaded.setHidden(False)

    def get_tiles(self, tiles):
        tiles = tiles.split("\r")

        return [
            (x, y)
            for x in range(len(tiles))
            for y in range(len(tiles[x]))
            if tiles[x][y] != "x"
        ]

    def alemao_room(self):
        if self.ui.move_wall.isChecked():

            for id, location in self.furnis["wall"]:
                x, y, x_offset, y_offset, position = self.alemao_location(
                    location)
                self.__ext.send_to_server(
                    '{out:MoveWallItem}{i:%d}{s:":w=%d,%d l=%d,%d %s"}'
                    % (id, x, y, x_offset, y_offset, position)
                )

                sleep(0.1)

        if self.ui.move_furni.isChecked():

            while self.toggled:
                for id in self.furnis["floor"]:
                    x, y = choice(self.tiles)

                    self.__ext.send_to_server(
                        "{out:MoveObject}{i:%s}{i:%s}{i:%s}{i:0}" % (id, x, y)
                    )

    def alemao_location(self, location):
        location = location.split()

        x, y = map(int, location[0][3:].split(","))
        x_offset, y_offset = map(int, location[1][2:].split(","))
        is_left = location[-1] == "l"

        if is_left:
            return x + 9, y, x_offset, y_offset, "r"
        return x, y + 9, x_offset, y_offset, "l"

    def can_start(self):
        if (not self.ui.move_furni.isChecked()) and (not self.ui.move_wall.isChecked()):
            QMessageBox.about(self.window, "Erro", "Escolha uma opção")
            return False

        if self.is_loaded():
            if self.ui.start.text() == "Parar":
                self.ui.start.setText("Iniciar")
                self.toggled = False

                self.ui.start.setStyleSheet(
                    'font: 75 9pt "Segoe UI";\n'
                    "font-weight: bold;\n"
                    "background-color: rgb(231, 179, 1);\n"
                    "border-style: outset;\n"
                    "border-radius: 5px;"
                )

                self.ui.move_furni.setChecked(False)
                self.ui.move_wall.setChecked(False)

                return False

            if self.ui.start.text() == "Iniciar":
                self.ui.start.setText("Parar")
                self.toggled = True

                self.ui.start.setStyleSheet(
                    'font: 75 9pt "Segoe UI";\n'
                    "font-weight: bold;\n"
                    "background-color: rgb(240, 0, 0);\n"
                    "border-style: outset;\n"
                    "border-radius: 5px;"
                )

                return True

    def can_stop(self, component):
        if self.ui.start.text() == "Parar":
            QMessageBox.about(self.window, "Erro", "Pressione o botão parar")
            component.setChecked(True)

    def is_loaded(self):
        if len(self.furnis["wall"]) + len(self.furnis["floor"]) > 0:
            return True

        QMessageBox.about(self.window, "Erro", "Reentre no quarto")
        return False
