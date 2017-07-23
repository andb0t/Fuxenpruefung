import os

from PIL import Image

image_paths = []
image_paths.append("../src/images/ger.png")
image_paths.append("../src/images/eng.png")
image_paths.append("../src/images/bay.png")

images = []
for image in image_paths:
    images.append(Image.open(image))

# make them the same size
size = 20, 15
for image in images:
    image.thumbnail(size, Image.ANTIALIAS)

# crop them and save them in pairs
for idx, image in enumerate(images):
    left = idx
    right = (idx + 1) % len(images)
    # crop half of each
    im1_cropped = images[left].crop((0, 0, 10, 20))
    im2_cropped = images[right].crop((10, 0, 20, 20))
    # patch them together
    output_im = Image.new('RGB', size)
    output_im.paste(im1_cropped, (0, 0))
    output_im.paste(im2_cropped, (10, 0))
    # save them
    dirname = os.path.dirname(image_paths[left]) + '/'
    basename = str(left) + str(right) + '.png'
    output_im_path = dirname + basename
    output_im.save(output_im_path)
