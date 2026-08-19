import numpy as np
import matplotlib.pyplot as plt

from optics import Ray, find_image


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


def draw_scene(ax, obj, lenses):
    ax.clear()

    # Physics
    rays = [Ray(*obj.unpack(), 0, lenses),
            Ray(*obj.unpack(), -0.25, lenses)]

    image = find_image(rays[0], rays[1])

    # text output
    print(f'Object position: {obj.pos}')
    print(f'Object height: {obj.h}')
    print()
    print(f'Image position: {image[0]}')
    print(f'Image height: {image[1]}')

    # object
    ax.plot([obj.pos, obj.pos], [0, obj.h], color="red")

    # lenses
    for i in range(len(lenses)):
        ax.axvline(x=lenses[i].pos, color="black")
        ax.plot(lenses[i].pos - lenses[i].f, 0, marker="o", color="black")
        ax.plot(lenses[i].pos + lenses[i].f, 0, marker="o", color="black")

    # rays
    draw_rays(ax, rays)

    # image
    if image[0] != np.inf:
        ax.plot([image[0], image[0]], [0, image[1]], color="blue")

    ax.set_title("Thin lenses")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.4)
    # ax.legend()

    plt.plot()
    plt.show()
