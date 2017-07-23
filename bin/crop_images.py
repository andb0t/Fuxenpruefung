import os

from PIL import Image

image_paths = []
image_paths.append("src/images/ger.png")
image_paths.append("src/images/eng.png")
image_paths.append("src/images/bay.png")

images = []
for image in image_paths:
    images.append(Image.open(image))

# make them the same size
size = 40, 31
MAX_PIX = 1000
for image in images:
    image.thumbnail(size, Image.ANTIALIAS)

# crop them and save them in pairs
for idx, image in enumerate(images):
    left = idx
    right = (idx + 1) % len(images)
    # crop half of each
    half_pix = int(size / 2)
    im1_cropped = images[left].crop((0, 0, half_pix, MAX_PIX))
    im2_cropped = images[right].crop((half_pix, 0, MAX_PIX, MAX_PIX))
    # patch them together
    output_im = Image.new('RGB', size)
    output_im.paste(im1_cropped, (0, 0))
    output_im.paste(im2_cropped, (half_pix, 0))
    # save them
    left_name = os.path.basename(image_paths[left]).split('.', 1)[0]
    right_name = os.path.basename(image_paths[right]).split('.', 1)[0]
    dirname = os.path.dirname(image_paths[left]) + '/'
    basename = str(left_name) + '_' + str(right_name) + '.png'
    output_im_path = dirname + basename
    output_im.save(output_im_path)
