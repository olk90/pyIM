import json
import sys
from pathlib import Path

from sqlalchemy import create_engine as ce

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget
from sqlalchemy.orm import declarative_base

from logic.model import create_tables
from logic.objectStore import update_history
from views.mainView import MainWindow

userHome = Path.home()
configDirectory = Path.joinpath(userHome, ".inventoryManager")
configFile = Path.joinpath(configDirectory, "config.json")

db = ce("sqlite:///pyIM.db")


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


def init_database():
    print("Connecting to database {}".format(db))
    db.connect()

    print("Initializing database")
    create_tables(db)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

    init_database()

    load_config_file()

    app = QApplication()
    form = QWidget(None)
    MainWindow(form)
    form.show()
    sys.exit(app.exec())
