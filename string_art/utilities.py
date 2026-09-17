from PIL import Image
import numpy as np
from math import floor, ceil, sqrt
from time import time


def numpy_to_image(array, size=None, mode="L"):
    array = array.astype(np.uint8)
    if size is not None:
        array = array.reshape(size)
    return Image.fromarray(array, mode=mode)


def crop_image(image: Image.Image, nails):
    nails = nails.copy()
    x_min = image.width
    x_max = 0
    y_min = image.height
    y_max = 0
    for nail in nails:
        x, y = nail
        if x < x_min: x_min = x
        if y < y_min: y_min = y
        if x > x_max: x_max = x
        if y > y_max: y_max = y

    for i in range(len(nails)):
        nails[i] = (nails[i][0] - x_min, nails[i][1] - y_min)
    return image.crop((floor(x_min)-1, floor(y_min)-1, ceil(x_max)+1, ceil(y_max)+1)), nails


def decompose_rgb_numpy(array: np.array):
    return array[:, 0], array[:, 1], array[:, 2]


def merge(image_r: Image.Image, image_g: Image.Image, image_b: Image.Image):
    data_r = np.array(image_r.getdata())
    data_r = data_r.reshape(image_r.height, image_r.width)
    data_g = np.array(image_g.getdata())
    data_g = data_g.reshape(image_g.height, image_g.width)
    data_b = np.array(image_b.getdata())
    data_b = data_b.reshape(image_b.height, image_b.width)
    data = np.zeros((image_r.height, image_r.width, 3))
    data[:, :, 0] = data_r
    data[:, :, 1] = data_g
    data[:, :, 2] = data_b
    return numpy_to_image(data, mode="RGB")


def string_art_glouton_gray_scale(I: np.ndarray, image_size, nails, string_width=0.1):
    start_time = time()
    # B is a blank image, with the same size of I
    B = np.ones(len(I)) * 255
    # lines[i][j] contains the modification due to the line going from i-th nail to j-th nail
    lines: list[list[np.ndarray | None]] = [[None for _ in range(len(nails))] for _ in range(len(nails))]
    for i in range(len(nails) - 1):
        for j in range(i + 1, len(nails)):
            line_vec = B.copy()
            add_line(line_vec, nails[i], nails[j], string_width, image_size[0])
            line_vec -= B
            lines[i][j] = line_vec
            lines[j][i] = line_vec


    Im = B
    best_err = error_numpy(Im, I)
    # index_i = np.random.randint(0, len(nails))
    index_i = 0
    nails_sequence = [index_i]
    while len(lines) > 0:
        best_j = -1
        for j in range(len(lines)):
            if lines[index_i][j] is None:
                continue
            err = error_numpy(Im + lines[index_i][j], I)
            if err < best_err:
                best_j = j
                best_err = err

        if best_j == -1:
            return Im, nails_sequence, time() - start_time
        Im = Im + lines[index_i][best_j]
        nails_sequence.append(best_j)
        lines[index_i][best_j] = None
        lines[best_j][index_i] = None
        index_i = best_j


def add_line(image: np.array, p1, p2, string_width, image_width):
    dy = p2[1] - p1[1]
    dx = p2[0] - p1[0]
    if dx == dy == 0: return image
    if abs(dx) > abs(dy):
        # If p2 is on the left from p1, switch p1 and p2
        if dx < 0:
            dx = -dx
            dy = -dy
            p1, p2 = p2, p1
        dy = dy / dx
        return add_hor_line(image, p1, dy, p2[0] - p1[0], string_width, image_width)
    else:
        # If p2 is on the top from p1, switch p1 and p2
        if dy < 0:
            dx = -dx
            dy = -dy
            p1, p2 = p2, p1
        dx = dx / dy
        return add_vert_line(image, p1, dx, p2[1] - p1[1], string_width, image_width)


def add_hor_line(image, start, dy, dist_x, width, image_width):
    volume = sqrt(dy * dy + 1) * width * 255
    y = start[1]
    for x in range(floor(start[0]), floor(start[0])+ceil(dist_x)):
        y += dy
        index_x = int(x)
        index_y = int(y)
        image[index_x + index_y * image_width] = max(image[index_x + index_y * image_width] - volume, 0)


def add_vert_line(image, start, dx, dist_y, width, image_width):
    volume = sqrt(dx * dx + 1) * width * 255
    x = start[0]
    for y in range(floor(start[1]), floor(start[1])+ceil(dist_y)):
        x += dx
        index_x = int(x)
        index_y = int(y)
        image[index_x + index_y * image_width] = max(image[index_x + index_y * image_width] - volume, 0)


def error_numpy(I1, I2):
    DIFF = I1 - I2
    return np.dot(DIFF, DIFF)
