'''genArt.py:
Reads the output from NEOS and renders
a tour in SVG.

Author: Kalyani Nagaraj
Last Updated: March 2022
'''

import os
import sys
import pickle


class tspArt:
    def __init__( self ):
        self.line_col = 'black'
        self.line_width = '1.5'

    def __write_svg_file( self, n):
        assert (n)

        # Get min and max co-ordinates
        column_max = max(self.city_dict.items(), key = lambda x: x[1][0])
        column_min = min(self.city_dict.items(), key = lambda x: x[1][0])
        c_min = column_min[1][0]
        c_max = column_max[1][0]
        row_max = max(self.city_dict.items(), key = lambda x: x[1][1])
        row_min = min(self.city_dict.items(), key = lambda x: x[1][1])
        r_min = row_min[1][1]
        r_max = row_max[1][1]
        buffer = int(3*float(self.line_width))

        s = open( self.svgfilename, 'w' )
        s.write('<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s">\n' % (str(c_max-c_min+2*buffer), str(r_max-r_min+2*buffer)) )
        # '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200">\n'
        s.write('    <polyline points="')
        line = n.readline()
        first_city = int(line.strip().split(' ')[0])
        first_city_coord = self.city_dict[first_city]
        s.write('%d, %d '  % ( first_city_coord[0]-c_min+buffer, first_city_coord[1]-r_min+buffer ))
        for line in n:
            city = int(line.strip().split(' ')[0])
            city_coord = self.city_dict[city]
            s.write('%d, %d '  % ( city_coord[0]-c_min+buffer, city_coord[1]-r_min+buffer ))

        s.write('%d, %d '  % ( first_city_coord[0]-c_min+buffer, first_city_coord[1]-r_min+buffer ))
        s.write('" style="fill:none;stroke:%s;stroke-width:%s" />\n' % (self.line_col, self.line_width))
        s.write('</svg>')

        s.close()
        n.close()

        return True

    def genSVG( self, neos_output_file, svg_file, pickled_dictnry_file, line_colour, line_width ):
        self.neosfilename = neos_output_file
        self.svgfilename = svg_file
        self.line_col = line_colour
        self.line_width = line_width

        n = open( self.neosfilename, 'r' )
        line = n.readline()

        with open(pickled_dictnry_file, 'rb') as p:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
            self.city_dict = pickle.load(p)

        ok = self.__write_svg_file( n )


if __name__ == '__main__':

    neos_output_file, svg_file, pickled_dictnry_file, line_colour, line_width  = sys.argv[1:]
    tA = tspArt()
    if not tA.genSVG( neos_output_file, svg_file, pickled_dictnry_file, line_colour, line_width):
        sys.exit( 1 )
