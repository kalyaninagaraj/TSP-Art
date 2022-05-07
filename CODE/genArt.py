import os
import sys
import pickle

class tspArt:
    def __init__( self ):
        self.line_col = 'black'
        self.line_width = '1.5'

    def __write_svg_file( self, n):
        assert (n)

        s = open( self.svgfilename, 'w' )
        s.write(
'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200">\n' +
'    <polyline points="')
        line = n.readline()
        first_city = int(line.strip().split(' ')[0])
        first_city_coord = self.city_dict[first_city]
        s.write('%d, %d '  % ( first_city_coord[0], first_city_coord[1] ))
        for line in n:
            city = int(line.strip().split(' ')[0])
            city_coord = self.city_dict[city]
            s.write('%d, %d '  % ( city_coord[0], city_coord[1] ))

        s.write('%d, %d '  % ( first_city_coord[0], first_city_coord[1]  ))
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
