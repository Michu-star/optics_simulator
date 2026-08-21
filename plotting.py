import numpy as np
import matplotlib.pyplot as plt

from optics import find_image


def draw_ray(ax, ray, color="grey"):
    for i in range(np.shape(ray.seg)[0] - 1):
        ax.plot([ray.seg[i, 0], ray.seg[i + 1, 0]], [ray.seg[i, 1], ray.seg[i + 1, 1]], color=color)


def draw_rays(ax, rays, delta=10, color="grey"):
    x_image, y_image = find_image(rays[0], rays[1])

    for j in range(len(rays)):
        draw_ray(ax, rays[j], color)

        x_last, y_last, s_last = rays[j].seg[-1]

        if x_image == np.inf:
            ax.plot([x_last, x_last + delta], [y_last, y_last + delta * s_last], color=color)
        else:
            ax.plot([x_last, x_image], [y_last, y_image], color=color)


def draw_scene(ax, system):

    # text output
    print(f'Object position: {system.obj.pos}')
    print(f'Object height: {system.obj.h}')
    print()
    print(f'Image position: {system.image[0]}')
    print(f'Image height: {system.image[1]}')

    # object
    ax.plot([system.obj.pos, system.obj.pos], [0, system.obj.h], color="red")

    # lenses
    for i in range(len(system.lenses)):
        ax.axvline(x=system.lenses[i].pos, color="black")
        ax.plot(system.lenses[i].pos - system.lenses[i].f, 0, marker="o", color="black")
        ax.plot(system.lenses[i].pos + system.lenses[i].f, 0, marker="o", color="black")

    # rays
    draw_rays(ax, system.rays)

    # image
    if system.image[0] != np.inf:
        ax.plot([system.image[0], system.image[0]], [0, system.image[1]], color="blue")

    ax.set_title("Thin lenses")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.4)
    # ax.legend()
