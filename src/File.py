from Chunk import Chunk
from adam7 import adam7
import pybin

magic_numbers = [137,80,78,71,13,10,26,10]

class File:
    """Container class for png file structure."""

    _contents = ''
    
    def __init__(self, ifname = None):
        # insert png file header's magic numbers
        for i in magic_numbers:
            # translate each integer to a single byte
            self._contents += pybin.itoc(i)
        if isinstance(ifname, str):
            infile = open(ifname, 'r')
            self._contents = infile.read()
            infile.close()

    def make_IHDR(self, width, height, bit_depth, color_type, interlace = False):
        """Makes png header chunk."""

        # initialize chunk
        IHDR = Chunk('IHDR',[])

        # store width, height in 4 bytes each (network order)
        IHDR.append(width, 4)
        IHDR.append(height, 4)

        # set bit depth and color type
        IHDR.append(bit_depth)
        IHDR.append(color_type)

        # set compression type and filter type (both always 0)
        IHDR.append(0)
        IHDR.append(0)

        # check if interlacing is desired
        if interlace:
            IHDR.append(1)
        else:
            IHDR.append(0)

        # append header chunk to file contents
        self._contents += IHDR.convert()

    def make_gAMA(self, gamma):
        """Creates the gAMA chunk that stores image gamma value."""
        
        # gAMA chunk contains only 4 bytes in it's data field.
        # those 4 bytes contain an unsigned int in network order equal to the
        # gamma value times 100,000.
        if gamma == None or not isinstance(gamma, int):
            return True
        gAMA = Chunk('gAMA', [])
        gAMA.append(gamma, 4)
        self._contents += gAMA.convert()
        return False

    def make_PLTE(self,palette):
        pass

    def make_tRNS(self, color, ctype):
        # tRNS is a simple chunk
        # layout depends on color type
        #   grayscale:
        #       2 bytes: grayscale sample
        #   paletted:
        #       1 byte: palette index value
        #   rgb:
        #       2 bytes: red sample
        #       2 bytes: green sample
        #       2 bytes: blue sample
        if ctype == 0 or ctype == 2:
            # grayscale or rgb
            tRNS = Chunk('tRNS', [])
            for sample in color:
                tRNS.append(sample, 2)
            return False
        if ctype == 3:
            # paletted, 1 alpha value per palette entry
            tRNS = Chunk('tRNS', [])
            for alphas in color:
                tRNS.append(alphas, 1)
            return False
        return True


    def make_bKGD(self, color, ctype):
        bKGD = None
        if ctype == 3:
            bKGD = Chunk('bKGD', [])
            bKGD.append(color, 1)
        if ctype in [0,4]:
            bKGD = Chunk('bKGD', [])
            bKGD.append(color, 2)
        if ctype in [2,6]:
            bKGD = Chunk('bKGD', [])
            for i in [0,1,2]:
                bKGD.append(color[i], 2)
        if bKGD != None:
            self._contents += bKGD.convert()
            return False
        return True


    # Clean this up for non-8 bit_depths
    #   and non-0 filters 
    def make_IDAT(self, image_array, interlace = False):
        """Converts image array into compressed bitstream within png file chunk structure."""

        # Check for interlacing, interlace if we want it
        if interlace:
            image = adam7(image_array)
        else:
            image = image_array[:]

        # initialize a new chunk
        IDAT = Chunk('IDAT',[])

        # scan each scanline in the image
        for scanlines in image:

            # filter the scanline
            IDAT.append(0) # no filtering yet

            # scan each pixel in the scanline
            for pixels in scanlines:

                #read each sample within the pixel
                for samples in pixels:
                    IDAT.append(samples)

        # compress contents and append to png file contents
        self._contents += IDAT.compress()
        
    def make_IEND(self):
        """Creates IEND chunk that terminates png file."""

        # initialize the chunk
        chunk = Chunk('IEND',[])

        # convert and append to file contents
        self._contents += chunk.convert()

    def write(self,of_name):
        """Writes png file to disk."""
        of = open(of_name, 'w')
        of.write(self._contents)
        of.close()
    
    def read(self):
        
        if self._contents[:8] != '\x89PNG\r\n\x1a\n':
            print 'not a png file'
            return []
        
        if not len(self._contents) > 8:
            print 'no chunks in file'
            return []
        
        contents = self._contents[8:]
        chunks = []
        counter = 1
        while len(contents) > 0:
            print 'reading chunk', counter
            counter += 1
            l = pybin.ntoi(contents[:4])
            chunk_string = contents[4:12 + l]
            chunks.append(Chunk().read(chunk_string))
            contents = contents[12 + l:]
            if len(contents) > 1 and chunks[-1]._name == 'IEND':
                print 'all chunks read, but still have', len(contents),
                print 'bytes left to read'
                break
        
        return chunks






