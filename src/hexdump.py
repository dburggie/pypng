from pybin import itoc, ctoi, itos, ntoi
from crc import crc32

magic_numbers = [137,80,78,71,13,10,26,10]

def hexdump(inname, outname = None, width = 20):
    
    infile = open(inname, 'r')
    contents = infile.read()
    infile.close()
    if outname == None:
        outname = inname + '.b'
    
    output = ''
    
    # check for magic bytes
    head = contents[:8]
    contents = contents[8:]
    for i in range(8):
        if not ctoi(head[i:i+1]) == magic_numbers[i]:
            print 'ERROR:',
            print '"{}" does not appear to be a PNG file'.format(filename)
            close(infile)
            return True
    for c in head:
        output += itos(ctoi(c)) + ' '
    output += '; PNG file magic numbers\n'
    
    while len(contents) >= 12:
        # each pass will read and print one chunk
        output += '\n'
        
        lenfield = contents[:4]
        length = ntoi(lenfield) + 12
        chunk = contents[:length]
        contents = contents[length:]
        
        name = chunk[4:8]
        data = chunk[8:-4]
        crcfield = chunk[-4:]
        crc = ntoi(crcfield)
        
        # verify data integrity
        bytefield = []
        for c in name:
            bytefield.append(ctoi(c))
        for c in data:
            bytefield.append(ctoi(c))
        if crc32(bytefield) == crc:
            crc = True
        else:
            crc = False
        
        # add length to output
        for c in lenfield:
            output += itos(ctoi(c))
            output += ' '
        output += '; chunk length: '
        output += str(length - 12)
        output += ' bytes\n'
        
        # add name to output
        for c in name:
            output += itos(ctoi(c))
            output += ' '
        output += '; chunk name: "'
        output += name
        output += '"\n\n; ##### Begin Chunk Data #####\n'
        
        # add chunk data
        counter = 0
        for c in data:
            output += itos(ctoi(c))
            counter += 1
            if counter == width:
                counter = 0
                output += '\n'
            else:
                output += ' '
        if counter != 0:
            output += '\n'
        output += '; ##### End Chunk Data #####\n\n'
        
        # add crc info
        for c in crcfield:
            output += itos(ctoi(c))
            output += ' '
        output += '; '
        if crc:
            output += 'crc verified'
        else:
            output += 'data section currupt'
            print '"{}" chunk has corrupt data section'.format(name)
        output += '\n\n'
    
    outfile = open(outname, 'w')
    outfile.write(output)
    outfile.close()
