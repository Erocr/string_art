from string_art import string_art, nails_circle_shape
from PIL import Image

image = Image.open("base_image.png").convert("L")
nails = nails_circle_shape((image.width, image.height), 50)
im, nails, t = string_art(image, nails, 0.1)
im.save("output/50_nails.png")
