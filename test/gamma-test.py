#!/usr/bin/python2
import pypng

gamma = 2.0
filename_in = 'test.png'
filename_out = 'gamma-{}.png'.format(gamma)

p = pypng.Png()
p.read(filename_in)
p.gamma_correct(gamma)
p.write(filename_out)
