from itos import itos
from ctoi import ctoi
from itoc import itoc

def _printable(i):
    if i >= 0x20 and i < 0x7f:
        return True
    else:
        return False

def _format_line(l):
    s = ''
    for i in l:
        if i == '':
            s +="   "
        else:
            s += "{} ".format(itos(i))
    s += '; "'
    for i in l:
        if i == '':
            continue
        elif _printable(i):
            s += itoc(i)
        else:
            s += ' '
    s += '"\n'
    return s


def unpack(if_name, of_name = 'output.b', width = 8):
    """Unpacks binary values in input_file to text in output_file."""
    
    # read contents of file
    input_file = open(if_name, 'r')
    contents = input_file.read()
    input_file.close()

    # accumulate reformatted file contents in 'output'
    output = ''
    line = []
    for char in contents:
        line.append(ctoi(char))
        if len(line) == width:
            output += _format_line(line)
            line = []
    #get that last line ready
    if len(line) > 0:
        for i in range(width - len(line)):
            line.append('')
        output += _format_line(line)
    
    # Print output to file
    output_file = open(of_name,'w')
    output_file.write(output)
    output_file.close()
    




