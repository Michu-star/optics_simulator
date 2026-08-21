from optics import Obj, Lens, OpticalSystem
from gui import draw_window


def main():
    lenses = [
        Lens(0, 2),
        Lens(10, -1)
    ]

    lenses.sort(key=lambda lens: lens.pos)

    obj = Obj(-100, 1)

    system = OpticalSystem(obj, lenses, [0, -0.25, 0.25])
    system.recalculate()

    draw_window(system)


if __name__ == "__main__":
    main()