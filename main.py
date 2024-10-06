# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    name = "Dir View"

    window = MainWindow(name)
    window.show()

    sys.exit(app.exec())
