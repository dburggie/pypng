_dict = {'0':0, '1':1, '2':2, '3':3, 
        '4':4,'5':5, '6':6, '7':7,
        '8':8, '9':9, 'a':10, 'b':11,
        'c':12, 'd':13, 'e':14, 'f':15}

def stoi(s):
    i = 0
    i += 16 * _dict[ s[0] ]
    i += _dict[ s[1] ] 
    return i
