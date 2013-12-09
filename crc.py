
crc_table = [0 for i in range(256)]

crc_constant = 0xedb88320

def _rightshift(u_l_int, n = 1):
    return u_l_int / (2 ** n)

# calculate crc_table
for n in range(256):
    c = n
    for k in range(8):
        if c & 1:
            c = (c / 2) ^ crc_constant
        else:
            c /= 2
    crc_table[n] = c

def _update(crc, bytefield):
    c = crc
    n = 0
    while n < len(bytefield):
        c = crc_table[(c ^ bytefield[n]) & 0xff] ^ (c / 256)
        n += 1
    return c

def crc32(bytefield):
    return _update(0xffffffff, bytefield) ^ 0xffffffff



