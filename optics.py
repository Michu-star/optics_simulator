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
    def __init__(self, position, f, d=0.0):
        self.pos = position # position of the left principal plane
        self.d = d          # distance between principal planes
        self.f = f

    # legacy methods
    '''
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
        '''


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

    def sort_lenses(self):
        self.lenses.sort(key=lambda lens: lens.pos)


def calculate_ray(lenses, ray):
    segments = [[ray.x_0, ray.y_0, ray.s_0]]

    for lens in lenses:
        x_before, y_before, s_before = segments[-1]

        x = lens.pos
        y = y_before + (x - x_before) * s_before
        s = -(y - lens.f * s_before) / lens.f

        if lens.d:
            segments.append([x, y, s_before])      # Arrival at H1
            segments.append([x + lens.d, y, s])    # Exit from H2 with new slope
        else:
            segments.append([x, y, s])

    return np.array(segments)


def find_image(ray1, ray2):
    x1_last, y1_last, s1_last = ray1.seg[-1]

    x2_last, y2_last, s2_last = ray2.seg[-1]

    if np.isclose(s1_last, s2_last):
        print("no image, rays parallel")
        x_image = np.inf
        y_image = np.inf * s1_last
        return x_image, y_image, None
    else:
        x_image = (y2_last - y1_last + s1_last * x1_last - s2_last * x2_last) / (s1_last - s2_last)
        y_image = y1_last + s1_last * (x_image - x1_last)

        if x_image > max(x1_last, x2_last):
            real = True
        else:
            real = False

        return x_image, y_image, real
