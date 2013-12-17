#!/usr/bin/python2

filename = 'test.png'
gamma = 1.00


import pypng
def sqrt(i):
    return int(i ** (0.5))

def dist(p1,p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


image = pypng.Png(256,256)
#image.set_gamma(gamma)

for i in range(256):
    for j in range(256):
        p = [i,j]
        color = [ dist(p,[0,0]) % 256,
                dist(p,[255,255]) % 256,
                dist(p,[127,127]) % 256]
        image.set_pixel(i,j,color)

image.write(filename)


