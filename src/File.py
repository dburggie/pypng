from Chunk import Chunk
from binedit import itoc
from adam7 import adam7

magic_numbers = [137,80,78,71,13,10,26,10]

class File:
    """Container class for png file structure."""

    _contents = ''
    
    def __init__(self):
        # insert png file header's magic numbers
        for i in magic_numbers:
            # translate each integer to a single byte
            self._contents += itoc(i)

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

    def make_tRNS(self, color):
        pass

    def make_bKGD(self, color):
        pass


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

        # open output file
        of = open(of_name, 'w')

        # write file to disk
        of.write(self._contents)

        # close output file
        of.close()







