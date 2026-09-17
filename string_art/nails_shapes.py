import numpy as np


def nails_circle_shape(size: tuple[int, int], nb_nails: int) -> list[tuple[int, int]]:
    """Generate evenly distributed nail positions along a circle.

    The circle is centered in the middle of the given dimensions
    and has a radius equal to half of the smallest dimension.
    The nails are evenly distributed around the circumference.

    :param size: A tuple containing the width and height of the area
        where the nails will be placed.
    :param nb_nails: The number of nails to generate.
    :return: A list of (x, y) coordinates representing the positions of
        the generated nails.
    """

    w, h = size
    res = []
    xc, yc = w / 2, h / 2
    r = min(w, h) / 2
    for i in range(nb_nails):
        t = i / nb_nails * 2 * np.pi
        res.append((xc + r * np.cos(t), yc + r * np.sin(t)))
    return res
