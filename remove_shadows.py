import os
import sys

from PIL import Image
import time
import shutil

path = "./vehicles"

print(path)

if len(sys.argv) >= 3:
    color = sys.argv[2]
    print(color)
    colorInt = int(color, 16)
else:
    colorInt = 0xA0000000


r0 = (colorInt >> 16) & 0xFF
g0 = (colorInt >> 8) & 0xFF
b0 = (colorInt >> 0) & 0xFF
a0 = (colorInt >> 24) & 0xFF
print("rgba = ({}, {}, {}, {})".format(r0, g0, b0, a0))

targetFolder = path + "\\new_icons"
print(targetFolder)

toDelete = os.path.join(targetFolder)
if os.path.isdir(toDelete):
    for f in os.listdir(toDelete):
        os.remove(os.path.join(targetFolder, f))
else:
    os.mkdir(targetFolder)

for f in os.listdir(path):
    if not os.path.isdir(f) and f[-len(".png"):] == ".png":
        try:
            original = os.path.join(path, f)
            copy = os.path.join(targetFolder, f)

            shutil.copyfile(original, copy)

            img = Image.open(copy)

            pixels = img.load()

            for y0 in range(0, img.height):
                for x0 in range(0, img.width):
                    r, g, b, a = img.getpixel((x0, y0))

                    if a != 255:
                        img.putpixel((x0, y0), (0, 0, 0, 0))

                img.putpixel((x0, y0), (r, g, b, a))

            img.save(copy)

        except IOError:
            print("Error for file {}".format(f))

print("done!")
