import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optics Simulator")
        self.setGeometry(0, 0, 800, 600)

        self.label = QLabel("Hello World")
        self.button1 = QPushButton("Click Me")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.slider_changed)


        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.button1)
        controls_layout.addWidget(self.slider)
        main_layout.addLayout(controls_layout)

        self.setLayout(main_layout)

    def slider_changed(self, value):
        print(value)


def draw_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

draw_window()