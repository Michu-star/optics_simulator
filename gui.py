import sys
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSlider, QVBoxLayout, QHBoxLayout, \
    QDoubleSpinBox, QGroupBox, QGridLayout, QScrollArea, QLineEdit

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from optics import Lens
from plotting import draw_scene

class EditableLensBox(QGroupBox):
    def __init__(self, lens, main_window, title=""):
        super().__init__(title)
        self.lens = lens
        self.main_window = main_window
        self.slider_N = main_window.slider_N
        self.setMouseTracking(True)
        self.setToolTip("Double-click title to rename")
        # Floating editor
        self.editor = QLineEdit(self)
        self.editor.setFixedSize(130, 22)
        self.editor.move(10, 1)  # <-- Fixed clipping!
        self.editor.setStyleSheet("""
            QLineEdit {
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                background-color: white;
                border: 1px solid #3498db;
                border-radius: 3px;
                padding: 1px 4px;
            }
        """)
        self.editor.hide()
        self.editor.editingFinished.connect(self.save_name)

        self.delete_btn = QPushButton("✕", self)
        self.delete_btn.setFixedSize(18, 18)
        self.delete_btn.setToolTip("Delete this lens")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                color: #95a5a6;
                font-weight: bold;
                font-size: 11px;
                background: transparent;
                border: 1px solid transparent;
                border-radius: 9px;
            }
            QPushButton:hover {
                color: #e74c3c;
                background-color: #fceae9;
                border-color: #e74c3c;
            }
        """)
        self.delete_btn.clicked.connect(lambda: self.main_window.remove_lens(self.lens, self))

        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(520)
        self.setContentsMargins(8, 12, 8, 4)  # Left, Top, Right, Bottom

        grid = QGridLayout()
        grid.setVerticalSpacing(3)

        # Position slider and spinbox
        pos_slider = QSlider(Qt.Orientation.Horizontal)
        pos_slider.setRange(-100 * self.slider_N, 100 * self.slider_N)
        pos_slider.setSingleStep(1)
        pos_slider.setValue(int(self.lens.pos * self.slider_N))

        pos_spinbox = QDoubleSpinBox()
        pos_spinbox.setRange(-100.0, 100.0)
        pos_spinbox.setSingleStep(1 / self.slider_N)
        pos_spinbox.setValue(self.lens.pos)

        pos_slider.valueChanged.connect(
            lambda value, lens=self.lens, spinbox=pos_spinbox: self.main_window.on_lens_pos_slider_changed(value, lens, spinbox)
        )
        pos_spinbox.valueChanged.connect(
            lambda value, lens=self.lens, slider=pos_slider: self.main_window.on_lens_pos_spinbox_changed(value, lens, slider)
        )

        # Focal length slider and spinbox
        f_slider = QSlider(Qt.Orientation.Horizontal)
        f_slider.setRange(-30 * self.slider_N, 30 * self.slider_N)
        f_slider.setSingleStep(1)
        f_slider.setValue(int(self.lens.f * self.slider_N))

        f_spinbox = QDoubleSpinBox()
        f_spinbox.setRange(-30.0, 30.0)
        f_spinbox.setSingleStep(1 / self.slider_N)
        f_spinbox.setValue(self.lens.f)

        f_slider.valueChanged.connect(
            lambda value, lens=self.lens, spinbox=f_spinbox: self.main_window.on_lens_f_slider_changed(value, lens, spinbox)
        )
        f_spinbox.valueChanged.connect(
            lambda value, lens=self.lens, slider=f_slider: self.main_window.on_lens_f_spinbox_changed(value, lens, slider)
        )

        # Thickness slider and spinbox
        d_slider = QSlider(Qt.Orientation.Horizontal)
        d_slider.setRange(0, 10 * self.slider_N)
        d_slider.setSingleStep(1)
        d_slider.setValue(int(self.lens.d * self.slider_N))

        d_spinbox = QDoubleSpinBox()
        d_spinbox.setRange(0.0, 10.0)
        d_spinbox.setSingleStep(1 / self.slider_N)
        d_spinbox.setValue(self.lens.d)

        d_slider.valueChanged.connect(
            lambda value, lens=self.lens, spinbox=d_spinbox: self.main_window.on_lens_d_slider_changed(value, lens, spinbox)
        )
        d_spinbox.valueChanged.connect(
            lambda value, lens=self.lens, slider=d_slider: self.main_window.on_lens_d_spinbox_changed(value, lens, slider)
        )

        # Add everything to grid
        grid.addWidget(QLabel("Position (x):"), 0, 0)
        grid.addWidget(pos_spinbox, 0, 1)
        grid.addWidget(pos_slider, 0, 2)

        grid.addWidget(QLabel("Focal Length (f):"), 1, 0)
        grid.addWidget(f_spinbox, 1, 1)
        grid.addWidget(f_slider, 1, 2)

        grid.addWidget(QLabel("Thickness (d):"), 2, 0)
        grid.addWidget(d_spinbox, 2, 1)
        grid.addWidget(d_slider, 2, 2)

        self.setLayout(grid)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.delete_btn.move(self.width() - 21, 8)

    def mouseMoveEvent(self, event):
        if event.pos().y() <= 20 and event.pos().x() <= 150:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.pos().y() <= 25:
            self.editor.setText(self.title())
            self.editor.show()
            self.editor.selectAll()
            self.editor.setFocus()
        super().mouseDoubleClickEvent(event)

    def save_name(self):
        new_name = self.editor.text().strip()
        if new_name:
            self.setTitle(new_name)
            self.lens.label = new_name
        self.editor.hide()

class MainWindow(QMainWindow):
    def __init__(self, optical_system):
        super().__init__()
        self.setWindowTitle("Optics Simulator")
        self.resize(1000, 700)

        self.setStyleSheet("""
            QLabel {
                        font-weight: bold;
                        color: #2c3e50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 6px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 6px;
                font-weight: bold;
                color: #2c3e50;
                background-color: #f3f3f3; /* keeps the border line from cutting through the text */
            }
        """)

        self.slider_N = 100
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
        # Create slider for object position
        self.object_position_slider = QSlider(Qt.Orientation.Horizontal)
        self.object_position_slider.setRange(-100 * self.slider_N, 100 * self.slider_N)
        self.object_position_slider.setSingleStep(1)
        self.object_position_slider.setValue(self.system.obj.pos * self.slider_N)
        self.object_position_slider.valueChanged.connect(self.on_obj_pos_slider_changed)

        # Create spinbox for object position
        self.object_position_spinbox = QDoubleSpinBox()
        self.object_position_spinbox.setRange(-100.0, 100.0)
        self.object_position_spinbox.setSingleStep(0.01)
        self.object_position_spinbox.setValue(self.system.obj.pos)
        self.object_position_spinbox.valueChanged.connect(self.on_obj_pos_spinbox_changed)

        self.image_info_label = QLabel()
        self.image_info_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 6px;
                font-size: 13px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)

    def create_layout(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.canvas, stretch=5)

        obj_img_layout = QHBoxLayout()
        obj_img_layout.addWidget(QLabel("Object Position"))
        obj_img_layout.addWidget(self.object_position_spinbox)
        obj_img_layout.addWidget(self.object_position_slider)
        obj_img_layout.addWidget(self.image_info_label)

        layout.addLayout(obj_img_layout)

        scroll_content = QWidget()
        self.lenses_row = QHBoxLayout(scroll_content)

        for i, lens in enumerate(self.system.lenses):
            name = lens.label if lens.label else f"Lens {i + 1}"
            lens_box = EditableLensBox(lens, self, name)
            self.lenses_row.addWidget(lens_box)

        self.add_btn = QPushButton("+ Add Lens")
        self.add_btn.setFixedSize(100, 120)
        self.add_btn.clicked.connect(self.add_lens)
        self.lenses_row.addWidget(self.add_btn)
        self.lenses_row.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_area.setFixedHeight(150)

        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        layout.addWidget(scroll_area)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_lens(self):
        new_lens_pos = self.system.lenses[-1].pos + 10
        if new_lens_pos > 100:
            new_lens_pos = 100
        new_lens = Lens(new_lens_pos, 10, 0,
                        label=f"Lens {len(self.system.lenses)+1}")

        self.system.lenses.append(new_lens)
        self.system.sort_lenses()

        box = EditableLensBox(new_lens, self, new_lens.label)
        idx = self.lenses_row.indexOf(self.add_btn)
        self.lenses_row.insertWidget(idx, box)

        self.system.recalculate()
        self.update_plot()

    def remove_lens(self, lens, lens_box):
        if len(self.system.lenses) <= 1:
            return

        if lens in self.system.lenses:
            self.system.lenses.remove(lens)

        lens_box.deleteLater()

        self.system.recalculate()
        self.update_plot()

    def on_obj_pos_slider_changed(self, value):
        pos = value / self.slider_N
        self.system.obj.pos = pos
        self.object_position_spinbox.blockSignals(True)
        self.object_position_spinbox.setValue(pos)
        self.object_position_spinbox.blockSignals(False)
        self.system.recalculate()
        self.update_plot()

    def on_obj_pos_spinbox_changed(self, value):
        self.system.obj.pos = value
        self.object_position_slider.blockSignals(True)
        self.object_position_slider.setValue(int(value * self.slider_N))
        self.object_position_slider.blockSignals(False)
        self.system.recalculate()
        self.update_plot()

    def on_lens_pos_slider_changed(self, value, lens, spinbox):
        pos = value / self.slider_N
        lens.pos = pos
        spinbox.blockSignals(True)
        spinbox.setValue(pos)
        spinbox.blockSignals(False)
        self.system.sort_lenses()
        self.system.recalculate()
        self.update_plot()

    def on_lens_pos_spinbox_changed(self, value, lens, slider):
        lens.pos = value
        slider.blockSignals(True)
        slider.setValue(int(value * self.slider_N))
        slider.blockSignals(False)
        self.system.sort_lenses()
        self.system.recalculate()
        self.update_plot()

    def on_lens_f_slider_changed(self, value, lens, spinbox):
        f = value / self.slider_N
        lens.f = f
        spinbox.blockSignals(True)
        spinbox.setValue(f)
        spinbox.blockSignals(False)
        self.system.recalculate()
        self.update_plot()

    def on_lens_f_spinbox_changed(self, value, lens, slider):
        lens.f = value
        slider.blockSignals(True)
        slider.setValue(int(value * self.slider_N))
        slider.blockSignals(False)
        self.system.recalculate()
        self.update_plot()

    def on_lens_d_slider_changed(self, value, lens, spinbox):
        d = value / self.slider_N
        lens.d = d
        spinbox.blockSignals(True)
        spinbox.setValue(d)
        spinbox.blockSignals(False)
        self.system.recalculate()
        self.update_plot()

    def on_lens_d_spinbox_changed(self, value, lens, slider):
        lens.d = value
        slider.blockSignals(True)
        slider.setValue(int(value * self.slider_N))
        slider.blockSignals(False)
        self.system.recalculate()
        self.update_plot()

    def update_plot(self):
        x_img, y_img, real = self.system.image
        if x_img == np.inf:
            text = "Image: at \u221e (collimated rays)"
        else:
            nature = "Real" if real else "Virtual"
            m = y_img / self.system.obj.h  # Magnification
            text = f"{nature} Image: x = {x_img:.2f}, h = {y_img:.2f}  |  " \
                   f"Magnification: {m:+.2f}\u00d7"
        self.image_info_label.setText(text)

        self.ax.clear()
        draw_scene(self.ax, self.system)
        self.canvas.draw()


def draw_window(optical_system):
    app = QApplication(sys.argv)
    window = MainWindow(optical_system)
    window.show()
    sys.exit(app.exec())
