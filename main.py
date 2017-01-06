from PIL import Image
import re

imagename = input("Give image file: ")

im = Image.open("palette.bmp")
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

palette = {}
palettenumber = 0

for rows in pixels:
    for pixel in rows:
        if pixel not in palette.keys():
            palette[pixel] = palettenumber
            palettenumber += 1
            if palettenumber == 16 or palettenumber == 31:
                palettenumber += 1

im = Image.open(imagename)
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

imagepalette = {}
palettenumber = 0
for rows in pixels:
    for pixel in rows:
        if pixel not in imagepalette.keys():
            imagepalette[pixel] = palettenumber
            palettenumber += 1


for color in imagepalette.keys():
    if color in palette.keys():
        imagepalette[color] = palette.get(color, "NONE")
    else:
        colorRGB = re.findall(r'\d+', str(color))
        diff = 999999
        closestcolor = ""
        for palcolor in palette.keys():
            palcolorRGB = re.findall(r'\d+', str(palcolor))

            d = ((int(colorRGB[0]) - int(palcolorRGB[0])) * 0.3) ** 2 + ((int(colorRGB[1]) - int(palcolorRGB[1])) * 0.59) ** 2 + ((int(colorRGB[2]) - int(palcolorRGB[2])) * 0.11) ** 2
            if d < diff:
                diff = d
                closestcolor = palette.get(palcolor, "NONE")
        imagepalette[color] = closestcolor


im = Image.open(imagename)
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

bitmap = []

for rows in pixels:
    for pixel in rows:
        bitmap.append(str(imagepalette.get(pixel, "NONE")))

transpbitmap =[]
for pixel in bitmap:
    if pixel == bitmap[0]:
        transpbitmap.append("255")
    else:
        transpbitmap.append(pixel)
bitmap = ",".join(bitmap)
transpbitmap = ",".join(transpbitmap)
print("Bitmap is\n" + imagename.split(".")[0], "db", bitmap + "\nWith transparency:\n" + imagename.split(".")[0], "db", transpbitmap)