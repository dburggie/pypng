#!/usr/bin/python2
import pypng

filename_in = 'read.png'
filename_out = 'read-edit.png'

red = [255,0,0]

png = pypng.Png()
if png.read(filename_in):
    print 'file read failed for some reason'
    exit()
else:
    print 'file read successful!'

w = png._width
h = png._height

for x in range(w):
    png.set_pixel(x, 0, red)
    png.set_pixel(x, 1, red)
    png.set_pixel(x, h - 2, red)
    png.set_pixel(x, h - 1, red)

for y in range( 2, h - 2, 1 ):
    png.set_pixel(0, y, red)
    png.set_pixel(1, y, red)
    png.set_pixel(w - 2, y, red)
    png.set_pixel(w - 1, y, red)

png.write(filename_out)


