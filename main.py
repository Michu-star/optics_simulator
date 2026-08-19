import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


class Obj:
    def __init__(self, position, height):
        self.pos = position
        self.h = height

    def unpack(self):
        return (self.pos, self.h)


class Ray:
    def __init__(self, x_initial, y_initial, slope_initial, lenses_to_propagate):
        self.x_0 = x_initial
        self.y_0 = y_initial
        self.s_0 = slope_initial
        self.seg = calculate_ray(lenses_to_propagate, self)


# Physics
class Lens:
    def __init__(self, position, f):
        self.pos = position
        self.f = f

    def calculate_image_pos(self, obj, ray_from_left=1):

        relative_pos = ray_from_left * (self.pos - obj.pos)

        if relative_pos == ray_from_left * self.f:
            return np.inf
        else:
            return self.pos + (1 / self.f - 1 / relative_pos) ** -1

    def calculate_image_h(self, obj, ray_from_left=1):
        image_pos = self.calculate_image_pos(obj, ray_from_left)
        return -obj.h * (image_pos - self.pos) / (self.pos - obj.pos)

    def calculate_image(self, obj, ray_from_left=1):
        return (self.calculate_image_pos(obj, ray_from_left), self.calculate_image_h(obj, ray_from_left))


# Geometry
def calculate_ray(lenses, ray):
    segments = np.zeros((len(lenses) + 1, 3))
    segments[0] = np.array([ray.x_0, ray.y_0, ray.s_0])

    for i in range(len(lenses)):
        x_before, y_before, s_before = segments[i]

        x = lenses[i].pos
        y = y_before + (x - x_before) * s_before
        s = -(y - lenses[i].f * s_before) / lenses[i].f

        segments[i + 1] = [x, y, s]

    return segments


def find_image(ray1, ray2):
    x1_last, y1_last, s1_last = ray1.seg[-1]

    x2_last, y2_last, s2_last = ray2.seg[-1]

    if np.isclose(s1_last, s2_last):
        print("no image, rays parallel")
        x_image = np.inf
        y_image = np.inf * s1_last
    else:
        x_image = x1_last + (y2_last - y1_last) / (s1_last - s2_last)
        y_image = y1_last + (x_image - x1_last) * s1_last

    return x_image, y_image


'''
def calculate_ray(lens, obj, h=0):
    image = Obj(*lens.calculate_image(obj, 1))

    start = np.array([obj.pos, obj.h])
    middle = np.array([lens.pos, h])
    end = np.array([image.pos, image.h])

    return np.array([start, middle, end])
'''


# Representation
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


lenses = [Lens(0,6),
          Lens(2,4),
          Lens(4,3)]
lenses.sort(key=lambda lens: lens.pos)

obj1 = Obj(-22, 1)

fig, ax = plt.subplots(figsize=(10, 7))

draw_scene(ax, obj1, lenses)
