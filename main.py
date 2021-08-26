import json
import sys
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget

from views.mainview import MainWindow

userHome = Path.home()
configDirectory = Path.joinpath(userHome, ".inventoryManager")


def write_history_file():
    pass


def load_config_file():
    if not configDirectory.exists():
        configDirectory.mkdir()
    configFile = Path.joinpath(configDirectory, "config.json")
    if configFile.exists():
        file = open(configFile)
        history = json.load(file)
        print(history)
    else:
        write_history_file()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    load_config_file()

    app = QApplication()
    form = QWidget(None)
    MainWindow(form)
    form.show()
    sys.exit(app.exec())
