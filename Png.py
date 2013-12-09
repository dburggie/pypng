from File import File

class Png:
    """Class containing methods for creation of png files."""
    
    # initial values
    _height = 1
    _width = 1
    _color_type = 2
    _bit_depth = 8
    _default_color = [0,0,0] # black
    _image = [[_default_color]]

    _background_color = None
    _transparent_color = None
    _text = None

    #methods

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


    def __init__(self, width, height, color_type = 2, bit_depth = 8):
        """Instantiate object."""
        self.set_dimensions(width,height)
        self.set_bit_depth(bit_depth)
        self.set_color_type(color_type)

