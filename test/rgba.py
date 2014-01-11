import pypng

i = pypng.Png(256,256,pypng.rgb_alpha)

for x in range(256):
    for y in range(256):
        c = (x + y) / 2
        i.set_pixel(x,y,[c, c / 2,255 - c,255 - c])

i.write('rgba.png')

