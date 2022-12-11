"""
Author: Kostiantyn Vasko
"""

import time

from headphones_hid import Headphones
from set_default_autio_device import DefaultAudioHandler
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox

import threading
import os
import sys
import ctypes

# for display icon at taskbar
app_id = 'byquip.default_audio_switcher.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

dirname = os.path.dirname(__file__)


class TrayApplication(QMainWindow):
    """
    Show message when the option is clicked
    """
    def __init__(self):
        super(TrayApplication, self).__init__()
        # Adding an icon
        self.icon2 = QIcon(os.path.join(dirname, 'hp.ico'))
        # self.setWindowIcon(self.icon2)
        self.icon = QIcon(os.path.join(dirname, "hp.png"))
        self.icon_pix = self.icon.pixmap(32, 32)
        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)

        # Creating the options
        self.menu = QMenu()

        self.option1 = QAction("info")
        self.quit = QAction("quit")

        self.menu.addAction(self.option1)
        self.menu.addAction(self.quit)

        self.option1.triggered.connect(self.show_message)
        self.quit.triggered.connect(self.quit_app)

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("Default Audio Device handler")
        self.tray.setVisible(True)
        self.tray.show()

    @staticmethod
    def quit_app():
        """
        quit app
        """
        QCoreApplication.exit()
        QCoreApplication.aboutToQuit()

    def show_message(self):
        """
        show message when the option is clicked
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(self.icon)
        msg.setWindowTitle("Info")
        msg.setText("Default Audio Device handler made by Kostiantyn Vasko\n"
                    "main functionality it's change default audio device if wifi headphones was switched on\off")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def gui():
    """
    gui
    """
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    _ = TrayApplication()
    sys.exit(app.exec())


def main_loop(dah: DefaultAudioHandler, hp: Headphones) -> None:
    """
    main loop
    :param dah: class DefaultAudioHandler
    :param hp: class Headphones
    """
    prev_state = False
    dah.set_def_ms()
    while True:
        time.sleep(1)
        if hp.powered and hp.powered != prev_state:
            dah.set_def_hp()
        elif not hp.powered and hp.powered != prev_state:
            dah.set_def_ms()
        prev_state = hp.powered

        # if QCoreApplication


def main_app():
    """
    main app
    """
    # TODO: add silence
    hp_speaker_name = "Наушники"
    hp_micro_name = "M. HyperX"
    main_dev_speaker_name = "Колонки"
    main_dev_micro_name = "M. WebCam"
    hp_name = [hp_speaker_name, hp_micro_name]
    main_dev_name = [main_dev_speaker_name, main_dev_micro_name]
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
