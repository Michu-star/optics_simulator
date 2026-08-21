from optics import Obj, Lens, OpticalSystem
from gui import draw_window


def main():
    lenses = [
        Lens(0, 20),
        Lens(10, -10)
    ]

    lenses.sort(key=lambda lens: lens.pos)

    obj = Obj(-10, 1)

    system = OpticalSystem(obj, lenses, [0, -0.1, 0.1])
    system.recalculate()

    draw_window(system)


if __name__ == "__main__":
    main()