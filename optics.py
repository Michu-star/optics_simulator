import numpy as np


class Obj:
    def __init__(self, position, height):
        self.pos = position
        self.h = height

    def unpack(self):
        return self.pos, self.h


class Ray:
    def __init__(self, x_initial, y_initial, slope_initial):
        self.x_0 = x_initial
        self.y_0 = y_initial
        self.s_0 = slope_initial
        self.seg = None


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
        return self.calculate_image_pos(obj, ray_from_left), self.calculate_image_h(obj, ray_from_left)


class OpticalSystem:
    def __init__(self, obj, lenses, ray_slopes):
        self.obj = obj
        self.lenses = lenses
        self.rays = []
        self.image = None

        for slope in ray_slopes:
            self.rays.append(Ray(*self.obj.unpack(), slope))

    def recalculate(self):
        for ray in self.rays:
            ray.x_0 = self.obj.pos
            ray.y_0 = self.obj.h
            ray.seg = calculate_ray(self.lenses, ray)

        self.image = find_image(self.rays[0], self.rays[1])


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
