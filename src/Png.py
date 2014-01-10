from File import File

class Png:
    """Class containing methods for creation of png files."""
    
    #### initial values ###
    _height = 1
    _width = 1
    _color_type = 2
    _bit_depth = 8
    _default_color = [0,0,0] # black
    _image = [[_default_color]]
    
    _palette = []
    _background_color = None
    _transparent_color = None
    _gamma = None
    _text = None
    
    ### methods ###
    
    def add_color_to_palette(self, color):
        if self._palette == None:
            raise self # adding to non-existent palette
        if len(self._palette) > 255:
            raise self # palette overflow
        self._palette.append(color)
        return [len(self._palette)]
    
    
    
    def verify_color(self,color):
        """Verifies that a color is in the right format for file parameters."""
        
        # dictionary of color types and associated sample numbers
        samples_per_pixel = {
                0 : 1,
                2 : 3,
                3 : 1,
                4 : 2,
                6 : 4
                }
        
        # calculate the maximum allowable sample value
        max_sample_value = 2 ** self._bit_depth - 1
        
        # check number of samples in color against value in dictionary
        if len(color) != samples_per_pixel[self._color_type]:
            return True
        
        # ensure all samples in color are less than the max
        for i in color:
            if i > max_sample_value:
                return True
        
        # color has passed inspection!
        return False
    
    
    
    def crop(self, x0, y0, x1, y1):
        """Crops image within rectangle between points (x0,y0) and (x1,y1)."""
        h = self._height
        w = self._width
        if x0 >= w or x1 + 1 >= w or y0 >= h or y1 + 1 >= h:
            return True
        
        # crop vertically taking a slice of _image member
        self._image = self._image[y0 : y1 + 1]
        
        # crop horizontally by slicing each line in _image member
        for line in self._image:
            line = line[x0 : x1 + 1]
    
    
    
    def set_pixel(self, x, y, color):
        """Sets pixel at (x,y)."""
        self._image[y][x] = color
    
    
    
    def get_pixel(self, x, y):
        """Returns the pixel at xy coordinate."""
        return self._image[y][x]
    
    
    
    def gamma_correct(self, gamma):
        """Gamma corrects every pixel in the image."""
        for scanlines in self._image:
            for pixels in scanlines:
                for i in range(len(pixels)):
                    pixels[i] = int(((pixels[i] / 256.0) ** gamma) * 256)
        return self
    
    
    
    def set_dimensions(self, width, height):
        """Sets image dimensions."""
        
        # dimensions in bounds?
        if width < 1 or height < 1:
            return True
        
        # adjust height
        if self._height < height:
            # new height is bigger, so we need to fill in empty pixels
            difference = height - self._height
            for j in range(difference):
                self._image.append([self._default_color for i in range(self._width)])
        else:
            # new height is smaller, crop height
            self._image = self._image[: height]
        self._height = height
        
        # adjust width
        if self._width < width:
            # new width is bigger, fill in empty pixels
            difference = width - self._width
            for scanlines in self._image:
                for i in range(difference):
                    scanlines.append(self._default_color)
        else:
            # new width is smaller, crop each line
            for line in self._image:
                line = line[: width]
        self._width = width
        
        return False
    
    
    
    def set_background(self, color):
        """Sets image background color."""
        self._background_color = color
    
    
    
    def set_default_color(self, color):
        """Sets image's default pixel color."""
        self._default_color = color
    
    
    
    def set_simple_alpha(self, color, alpha = 0):
        if self._color_type in [4, 6]:
            return True
        elif self._color_type == 3:
            # handle simple transparency in paletted case
            index = color[0]
            if index > 255 or index < 0:
                return True
            dif = index - len(self._simple_alpha)
            for i in range(dif + 1):
                self._simple_alpha.append(255)
            self._simple_alpha[index] = alpha
            return False
        elif self._color_type in [0,2]:
            self._simple_alpha = color
            return False
        else:
            return True
    
    def set_gamma(self, gamma):
        """Set's image's gamma value."""
        if gamma == None:
            self._gamma = None
            return False
        if not isinstance(gamma, float):
            return True
        self._gamma = int(gamma * 100000)
        return False
    
    
    
    def set_bit_depth(self, bit_depth):
        """Verifies bit depth and color type get along, then sets bit depth."""
        if bit_depth in [1,2,4,8]:
            if self._color_type in [0,3]:
                self._bit_depth = bit_depth
                return False
            else:
                return True
        if bit_depth in [8,16]:
            if self._color_type in [0,2,4,6]:
                self._bit_depth = bit_depth
                return False
            else:
                return True
        return True
    
    
    
    def set_color_type(self, color_type):
        """Sets image color type."""
        if not color_type in [0,2,3,4,6]:
            return True
        self._color_type = color_type
        if color_type == 3:
            self._palette = []
        else:
            self._palette = None
        if self.set_bit_depth(self._bit_depth):
            self._bit_depth = 8
        return False
    
    
    
    def write(self,of,interlaced = False):
        """Writes image to file."""
        imagefile = File()
        imagefile.make_IHDR(
                self._width,
                self._height,
                self._bit_depth,
                self._color_type
                )
        
        # handle special case blocks
        if self._gamma != None:
            imagefile.make_gAMA(self._gamma)
        if self._color_type == 3:
            imagefile.make_PLTE(self._palette)
        if not self._background_color == None:
            imagefile.make_bKGD(self._background)
        if not self._transparent_color == None:
            imagefile.make_tRNS(self._transparent_color)
        
        # make data block
        imagefile.make_IDAT(self._image)
        
        # make text
        if not self._text == None:
            imagefile.make_tEXT(self._text)
        
        # end file
        imagefile.make_IEND()
        
        imagefile.write(of)
        return True
    
    
    
    def _parse_header(self, chunk):
        width_array = chunk._data[:4]
        width = 0
        for i in width_array:
            width *= 256
            width += i
        height_array = chunk._data[4:8]
        height = 0
        bit_depth = chunk._data[8]
        if bit_depth != 8:
            print 'can only read bit_depth 8 at this time'
            return True
        color_type = chunk._data[9]
        if color_type != 2:
            print 'can only read simple rgb images at this time'
            return True
        for i in height_array:
            height *= 256
            height += i
        if chunk._data[10] != 0:
            print 'bad compression type byte in', ifname
            return True
        if chunk._data[11] != 0:
            print 'bad filter type byte in', ifname
            return True
        interlace = chunk._data[12]
        if interlace == 1:
            print 'cannot read interlaced images at this time'
            return True
        self.set_dimensions(width, height)
        self.set_bit_depth(bit_depth)
        self.set_color_type(color_type)
        return False
    
    
    
    def _parse_data(self, chunk):
        """Parses data chunk while reading file."""
        offset = 1
        for y in range(self._height):
#            print 'getting line',y,'of',self._height
            for x in range(self._width):
                pixel = []
                for s in range(3):
                    pixel.append(chunk._data[offset])
                    offset += 1
                self.set_pixel(x,y,pixel)
            offset += 1
        return False
    
    
    
    def _parse_chunk(self, chunk):
        name = chunk._name
        if not name in ['IHDR','IEND','IDAT']:
            print name, 'chunk cannot be read in this version'
            return True
        if name == 'IHDR':
            return self._parse_header(chunk)
        if name == 'IDAT':
            return self._parse_data(chunk)
        return False
    
    
    
    def read(self, ifname):
        """Returns new Png instance containing contents of png file on disk."""
        imagefile = File(ifname)
        chunks = imagefile.read()
        if len(chunks) != 3:
            print 'png file must consist exactly of',
            print 'IHDR, IDAT, and IEND chunks'
            return True
        for c in chunks:
            if self._parse_chunk(c):
                return True
        return False
    
    
    
    def __init__(self, width = 1, height = 1, color_type = 2, bit_depth = 8):
        """Instantiate object."""
        self.set_dimensions(width,height)
        self.set_bit_depth(bit_depth)
        self.set_color_type(color_type)

