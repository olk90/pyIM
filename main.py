import json
import sys
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget

from logic.database import init_database
from logic.files import update_history
from views.mainView import MainWindow

userHome = Path.home()
configDirectory = Path.joinpath(userHome, ".pyIM")
configFile = Path.joinpath(configDirectory, "config.json")


def write_config_file():
    config_dict = {
        "history": []
    }
    config = json.dumps(config_dict, indent=4)
    with open(configFile, "w") as f:
        f.write(config)
        f.close()


def load_config_file():
    if not configDirectory.exists():
        configDirectory.mkdir()
    if configFile.exists():
        file = open(configFile)
        history = json.load(file)
        update_history(history)
    else:
        write_config_file()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    init_database()
    load_config_file()

    app = QApplication()
    form = QWidget(None)
    MainWindow(form)
    form.show()
    sys.exit(app.exec())
