from .utilities import *


def string_art(image: Image.Image, nails, string_width=0.1):
    image, nails = crop_image(image, nails)
    I = np.array(image.get_flattened_data())
    image_size = (image.width, image.height)

    if image.mode == "L" or image.mode == "1":
        im, nails_sequence, t = string_art_glouton_gray_scale(I, image_size, nails, string_width)
        return numpy_to_image(im, (image_size[1], image_size[0]), "L"), nails_sequence, t

    elif image.mode == "RGB":
        Ir, Ig, Ib = decompose_rgb_numpy(I)
        im_r, nails_r, t_r = string_art_glouton_gray_scale(Ir, image_size, nails, string_width)
        im_g, nails_g, t_g = string_art_glouton_gray_scale(Ig, image_size, nails, string_width)
        im_b, nails_b, t_b = string_art_glouton_gray_scale(Ib, image_size, nails, string_width)

        # Merging the images
        im = np.zeros(im_r.shape + (3,))
        im[:, 0] = im_r
        im[:, 1] = im_g
        im[:, 2] = im_b

        # Merging the nail sequences
        nails = ["R"] + nails_r + ["G"] + nails_g + ["B"] + nails_b

        # Merging the times
        t = t_r + t_g + t_b

        return numpy_to_image(im, (image_size[1], image_size[0], 3), "RGB"), nails, t


