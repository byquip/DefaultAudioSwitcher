import time

from headphones_hid import Headphones
from set_default_autio_device import DefaultAudioHandler
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox

import threading
import os
import sys
dirname = os.path.dirname(__file__)


class TrayApplication(QMainWindow):
    def __init__(self):
        super(TrayApplication, self).__init__()
        # Adding an icon
        self.icon = QIcon(os.path.join(dirname, "hp.png"))
        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)

        # Creating the options
        self.menu = QMenu()

        self.option1 = QAction("info")
        self.quit = QAction("quit")

        self.menu.addAction(self.option1)
        self.menu.addAction(self.quit)

        self.option1.triggered.connect(lambda: self.show_message())
        self.quit.triggered.connect(lambda: self.quit_app())

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("Default Audio Device handler")
        self.tray.setVisible(True)
        self.tray.show()

    @staticmethod
    def quit_app():
        QCoreApplication.exit()
        QCoreApplication.aboutToQuit()

    @staticmethod
    def show_message():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
        msg.setText("Default Audio Device handler made by Kostiantyn Vasko\n"
                    "main functionality it's change default audio device if wifi headphones was switched on\off")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def gui():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    _ = TrayApplication()
    sys.exit(app.exec())


def main_loop(dah: DefaultAudioHandler, hp: Headphones) -> None:
    prev_state = False
    while True:
        time.sleep(1)
        if hp.powered and hp.powered != prev_state:
            dah.set_def_hp()
        elif not hp.powered and hp.powered != prev_state:
            dah.set_def_ms()
        prev_state = hp.powered

        # if QCoreApplication


def main_app():
    hp_name = "Speakers"
    main_dev_name = "1 - VS278"
    dah = DefaultAudioHandler(main_dev_name, hp_name)

    VID, PID = (2385, 5907)
    hp = Headphones(VID, PID)

    listen_trd = threading.Thread(target=hp.listen)
    main_trd = threading.Thread(target=main_loop, args=(dah, hp,))
    gui_trd = threading.Thread(target=gui)

    listen_trd.start()
    main_trd.start()
    gui_trd.start()


if __name__ == '__main__':
    main_app()
