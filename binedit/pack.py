from itoc import itoc
from ctoi import ctoi
from stoi import stoi

def _whitespace(c):
    i = ctoi(c)
    if i < 0x21 or i > 0x7e:
        return True
    return False

def _scan_line(line,c):
    for i in range(len(line)):
        if line[i] == c or line[i] == '\n':
            break
    return i

def _parse_line(line):

    # scan line for comment character
    line_end = _scan_line(line, ';')

    line = line[:line_end]
    output = ['']
    counter = 0
    for c in line:
        if _whitespace(c):
            continue
        if len(output[counter]) == 2:
            counter += 1
            output.append('')
        output[counter] += c
    return output
    


def pack(if_name, of_name = 'output.bin'):
    """Packs text file of hex values into a binary file format."""

    # open input file
    infile = open(if_name, 'r')

    # initialize output accumulator
    output = ''

    # parse file line by line, accumulating output as we go
    line = infile.readline()
    while line != '':
        for s in _parse_line(line):
            output += itoc( stoi(s) )
        line = infile.readline()

    infile.close()

    # output to file
    outfile = open(of_name, 'w')
    outfile.write(output)
    outfile.close()





