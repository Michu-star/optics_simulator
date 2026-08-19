import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optics Simulator")
        self.setGeometry(0, 0, 800, 600)


def draw_scene():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

draw_scene()