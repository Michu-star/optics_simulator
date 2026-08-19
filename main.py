import matplotlib.pyplot as plt

from optics import Obj, Lens, OpticalSystem
from plotting import draw_scene


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

    fig, ax = plt.subplots(figsize=(10, 7))
    draw_scene(ax, system)


if __name__ == "__main__":
    main()