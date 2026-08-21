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

        self.lens_position_sliders = []

        for i, lens in enumerate(self.system.lenses):
            slider = QSlider(Qt.Orientation.Horizontal)

            slider.setRange(-400, 400)
            slider.setSingleStep(1)

            # to allow for the step size of 0.25 the slider value is 4 times the position of the object
            slider.setValue(self.system.lenses[i].pos * 4)

            self.lens_position_sliders.append(slider)

            slider.valueChanged.connect(
                lambda value, i=i: self.lens_position_changed(value, i)
            )

    def create_layout(self):
        central_widget = QWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.canvas)
        layout.addWidget(self.object_position_slider)

        for lens_slider in self.lens_position_sliders:
            layout.addWidget(lens_slider)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def object_position_changed(self, value):
        self.system.obj.pos = value / 4
        self.system.recalculate()

        self.update_plot()

    def lens_position_changed(self, value, i):
        self.system.lenses[i].pos = value / 4
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
