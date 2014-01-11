from pypng import Png

def dist(x,y):
    return (x ** 2.0 + y ** 2.0) ** 0.5

i = Png(256, 256)
for x in range(256):
    for y in range(256):
        d = dist(x - 128, y - 128)
        if d < 64:
            i.set_pixel(x,y,[255,0,0])
        else:
            i.set_pixel(x,y,[0,0,0])
if i.set_simple_alpha([0,0,0]):
    print 'error in set_simple_alpha method of Png class'
i.write('simple_alpha.png')
