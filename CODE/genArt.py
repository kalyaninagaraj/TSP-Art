'''genArt.py:
Reads the output from NEOS and renders a tour in SVG.

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

        # Get min and max of co-ordinates to frame the image in Inkscape
        column_max = max(self.city_dict.items(), key = lambda x: x[1][0])
        column_min = min(self.city_dict.items(), key = lambda x: x[1][0])
        c_min = column_min[1][0]
        c_max = column_max[1][0]
        row_max = max(self.city_dict.items(), key = lambda x: x[1][1])
        row_min = min(self.city_dict.items(), key = lambda x: x[1][1])
        r_min = row_min[1][1]
        r_max = row_max[1][1]
        buffer = int(3*float(self.line_width))

        # Create an xml preamble for the SVG file
        s = open( self.svgfilename, 'w' )
        s.write('<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s">\n' % (str(c_max-c_min+2*buffer), str(r_max-r_min+2*buffer)) ) # '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200">\n'

        # Enter city coordinates in sequence (as they appear in the final tour) to constuct a polyline in Inkscape
        # Ensure that the polyline ends at the first city in the tour
        city_count = 0
        s.write('    <polyline points="')
        line = n.readline()
        first_city = int(line.strip().split(' ')[0])
        first_city_coord = self.city_dict[first_city]
        s.write('%d,%d '  % ( first_city_coord[0]-c_min+buffer, first_city_coord[1]-r_min+buffer ))
        city_count += 1
        for line in n:
            city = int(line.strip().split(' ')[0])
            city_coord = self.city_dict[city]
            s.write('%d,%d '  % ( city_coord[0]-c_min+buffer, city_coord[1]-r_min+buffer ))
            city_count += 1
        s.write('%d,%d" '  % ( first_city_coord[0]-c_min+buffer, first_city_coord[1]-r_min+buffer ))
        s.write('style="fill:none;stroke:%s;stroke-width:%s" />\n' % (self.line_col, self.line_width))
        s.write('</svg>')

        # Close the SVG file and the NEOS output file
        s.close()
        n.close()

        if city_count != len(self.city_dict):
            sys.stderr.write( 'Tour returned by solver is either too short or too long\n#Cities in tour = %d\n#Cities in image (PBM) file = %d\n' % (city_count, len(self.city_dict)) )
            return False
        return True


    def genSVG( self, neos_output_file, svg_file, pickled_dictnry_file, line_colour, line_width ):
        self.neosfilename = neos_output_file
        self.svgfilename = svg_file
        self.line_col = line_colour
        self.line_width = line_width

        n = open( self.neosfilename, 'r' )
        line = n.readline()  # Read the first line containing city count

        with open(pickled_dictnry_file, 'rb') as p:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
            self.city_dict = pickle.load(p)

        citycount = int(line.strip().split(' ')[0])
        if citycount == len(self.city_dict):
            ok = self.__write_svg_file( n )
        else:
            sys.stderr.write('Cities in tour and input file do not match\n')
            ok = False

        return ok

if __name__ == '__main__':

    neos_output_file, svg_file, pickled_dictnry_file, line_colour, line_width  = sys.argv[1:]
    tA = tspArt()
    if not tA.genSVG( neos_output_file, svg_file, pickled_dictnry_file, line_colour, line_width):
        sys.exit( 1 )
