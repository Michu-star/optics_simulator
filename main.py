import matplotlib.pyplot as plt

from optics import Obj, Lens, OpticalSystem
from plotting import draw_scene
from gui import draw_window


def main():
    lenses = [
        Lens(0, 6),
        Lens(2, 4),
        Lens(4, 3)
    ]

    lenses.sort(key=lambda lens: lens.pos)

    obj = Obj(-22, 1)

    system = OpticalSystem(obj, lenses, [0, -0.25, 0.25])
    system.recalculate()

    draw_window(system)


if __name__ == "__main__":
    main()