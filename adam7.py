# adam7 interlacing takes an image in scanlines and breaks it up into 7 sub
# images so they can be rendered more quickly
# pass 1: indexes that are 0 mod 8 in 0 mod 8 scanlines
# pass 2: indexes that are 4 mod 8 in 0 mod 8 scanlines
# pass 3: indexes that are 0 mod 4 in 4 mod 8 scanlines
# pass 4: indexes that are 2 and 6 mod 8 in 0 mod 4 scanlines
# pass 5: indexes that are 0 mod 2 in 2 and 6 mod 8 scanlines
# pass 6: indexes that are 1 mod 2 in 0 mod 2 scanlines
# pass 7: all indexes in 1 mod 2 scanlines
#
# 16462646
# 77777777
# 56565656
# 77777777
# 36463646
# 77777777
# 56565656
# 77777777
#
# pass 1:   pass 2:   pass 3:   pass 4:
# X-------  ----X---  --------  --X---X-
# --------  --------  --------  --------
# --------  --------  --------  --------
# --------  --------  --------  --------
# --------  --------  X---X---  --X---X-
# --------  --------  --------  --------
# --------  --------  --------  --------
# --------  --------  --------  --------
#
# pass 5:   pass 6:   pass 7:
# --------  -X-X-X-X  --------
# --------  --------  XXXXXXXX
# X-X-X-X-  -X-X-X-X  --------
# --------  --------  XXXXXXXX
# --------  -X-X-X-X  --------
# --------  --------  XXXXXXXX
# X-X-X-X-  -X-X-X-X  --------
# --------  --------  XXXXXXXX
# 



def adam7(image):

    height = len(image)
    width = len(image[0])
    a = []
    # pass 1
    for j in range(0, height, 8):
        a.append([])
        for i in range(0, width, 8):
            a[-1].append(image[j][i])

    # pass 2
    for j in range(0, height, 8):
        a.append([])
        for i in range(4, width, 8):
            a[-1].append(image[j][i])

    # pass 3
    for j in range(4, height, 8):
        a.append([])
        for i in range(0, width, 4):
            a[-1].append(image[j][i])

    # pass 4
    for j in range(0, height, 4):
        a.append([])
        for i in range(2, width, 4):
            a[-1].append(image[j][i])

    # pass 5
    for j in range(2, height, 4):
        a.append([])
        for i in range(0, width, 2):
            a[-1].append(image[j][i])

    # pass 6
    for j in range(0, height, 2):
        a.append([])
        for i in range(1, width, 2):
            a[-1].append(image[j][i])

    # pass 7
    for j in range(1, height, 2):
        a.append([])
        for i in range(0, width):
            a[-1].append(image[j][i])

    return a
