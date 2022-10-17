import sys
from datetime import date

from PySide6 import QtCore
from PySide6.QtCore import QFile, QCoreApplication
from PySide6.QtWidgets import QComboBox, QSpinBox


def load_ui_file(filename):
    ui_file = QFile(filename)
    if not ui_file.open(QFile.ReadOnly):
        print("Cannot open {}: {}".format(filename, ui_file.errorString()))
        sys.exit(-1)
    return ui_file


def translate(context, text):
    return QCoreApplication.translate(context, text, None)


def get_min_date():
    today = date.today()
    month_abbr = today.strftime("%b")
    min_year = today.year
    return month_abbr, min_year


def configure_next_mot(month_cb: QComboBox, year_sp: QSpinBox):
    min_date = get_min_date()
    index = month_cb.findText(min_date[0], QtCore.Qt.MatchFixedString)
    if index >= 0:
        month_cb.setCurrentIndex(index)
    year_sp.setMinimum(min_date[1])
