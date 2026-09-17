import numpy as np


def nails_circle_shape(size, nb_nails):
    w, h = size
    res = []
    xc, yc = w / 2, h / 2
    r = min(w, h) / 2
    for i in range(nb_nails):
        t = i / nb_nails * 2 * np.pi
        res.append((xc + r * np.cos(t), yc + r * np.sin(t)))
    return res
