from string_art import string_art, nails_circle_shape
from PIL import Image

for i in range(1, 5):
    image = Image.open("base_image.jpg").convert("L")
    nails = nails_circle_shape((image.width, image.height), i * 50)
    im, nails, t = string_art(image, nails, 0.1)
    im.save(f"output/{i*50}_nails.png")
