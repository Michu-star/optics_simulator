import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from plotting import draw_scene

class MainWindow(QMainWindow):
    def __init__(self, optical_system):
        super().__init__()
        self.setWindowTitle("Optics Simulator")
        self.setGeometry(0, 0, 800, 600)

        self.system = optical_system

        self.create_plot()
        self.create_controls()
        self.create_layout()

        self.update_plot()

    def create_plot(self):
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.subplots()

    def create_controls(self):
        self.object_position_slider = QSlider(Qt.Orientation.Horizontal)

        self.object_position_slider.setRange(-400, 400)
        self.object_position_slider.setSingleStep(1)

        # to allow for the step size of 0.25 the slider value is 4 times the position of the object
        self.object_position_slider.setValue(self.system.obj.pos * 4)

        self.object_position_slider.valueChanged.connect(
            self.object_position_changed
        )

    def create_layout(self):
        central_widget = QWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.canvas)
        layout.addWidget(self.object_position_slider)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def object_position_changed(self, value):
        self.system.obj.pos = value / 4
        self.system.recalculate()

        self.update_plot()

    def update_plot(self):
        self.ax.clear()

        draw_scene(self.ax, self.system)

        self.canvas.draw()


def draw_window(optical_system):
    app = QApplication(sys.argv)
    window = MainWindow(optical_system)
    window.show()
    sys.exit(app.exec())
