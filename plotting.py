import numpy as np
import matplotlib.pyplot as plt

from optics import find_image


def draw_ray(ax, ray, color="grey"):
    for i in range(np.shape(ray.seg)[0] - 1):
        ax.plot([ray.seg[i, 0], ray.seg[i + 1, 0]], [ray.seg[i, 1], ray.seg[i + 1, 1]], color=color)


def draw_rays(ax, rays, delta, color="grey"):
    x_image, y_image, real = find_image(rays[0], rays[1])

    for j in range(len(rays)):
        draw_ray(ax, rays[j], color)

        x_last, y_last, s_last = rays[j].seg[-1]

        # 1. Physical outgoing ray: always travels forward (+x)
        if real and x_image > x_last:
            # Passes through the real image and continues forward
            ax.plot([x_last, x_image], [y_last, y_image], color=color)
            ax.plot([x_image, x_image + delta], [y_image, y_image + delta * s_last], color=color)
        else:
            # Parallel or virtual: ray continues propagating forward into space
            ax.plot([x_last, x_last + delta], [y_last, y_last + delta * s_last], color=color)

        # 2. Virtual image projection: dashed line traced backward to the apparent origin
        if real is False and x_image != np.inf:
            ax.plot([x_image, x_last], [y_image, y_last], color=color, linestyle="--", alpha=0.6)


def draw_scene(ax, system, delta=10):

    # text output
    print(f'Object position: {system.obj.pos}')
    print(f'Object height: {system.obj.h}')
    print()
    print(f'Image position: {system.image[0]}')
    print(f'Image height: {system.image[1]}')

    # object
    ax.plot([system.obj.pos, system.obj.pos], [0, system.obj.h], color="red")

    # lenses
    for i, lens in enumerate(system.lenses):
        if lens.d:
            ax.axvline(x=lens.pos, color="black")
            ax.axvline(x=lens.pos + lens.d, color="black")
            ax.axvspan(lens.pos, lens.pos + lens.d, alpha=0.15, color='cyan')
            ax.plot(lens.pos - lens.f, 0, marker="o", color="black")
            ax.plot(lens.pos + lens.d + lens.f, 0, marker="o", color="black")
        else:
            ax.axvline(x=lens.pos, color="black")
            ax.plot(lens.pos - lens.f, 0, marker="o", color="black")
            ax.plot(lens.pos + lens.f, 0, marker="o", color="black")

    # rays
    draw_rays(ax, system.rays, delta)

    # image
    if system.image[0] != np.inf:
        ax.plot([system.image[0], system.image[0]], [0, system.image[1]], color="blue")

    ax.set_title("Optics Simulator")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.4)
    # ax.legend()
