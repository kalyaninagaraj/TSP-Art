'''genCoordinates.py:
Obtains pixel coordinates from PBM file
and saves to a text file

Author: Kalyani Nagaraj
Last Updated: March 2022
'''
import os
import sys
import pickle

class tspCityCoord:
    def __init__( self ):
        self.width = 0
        self.height = 0


    def __load_pbm_p1( self, f ):
        assert (self.width > 0) and (self.height > 0)
        assert (f)

        self.citydict = {}
        column = 0
        row = 1

        self.city_count = 0   # Start from 0th city
        for line in f:
            line = line.strip()
            if ( line[0] == '' ) or ( line[0] == '#' ):
                continue
            if row >= self.height + 1:
                sys.stderr.write( 'Too much data in %s\n' % self.pbmfile )
                return False

            for i in range(0, len(line)):
                if line[i] == '1':
                    self.citydict[self.city_count]= ( column, row )
                    self.city_count += 1
                elif line[i] != '0':
                    sys.stderr.write( 'Invalid content in %s\n' % self.pbmfile )
                    return False
                column += 1

                # Reached end of row?
                if column >= self.width:
                    # Finished a row, move down to the next row
                    column = 0
                    row += 1 # row -= 1

        # Perform a sanity check: we should be at the start of row=height+1
        # If OK, then pickle the dictionary of coordinates
        if ( column == 0 ) and ( row == self.height +1 ):
            p = open( self.pickle_file, "wb" )
            pickle.dump( self.citydict, p )
            p.close()
            return True

        # Something's gone wrong if the rows ended prematurely
        sys.stderr.write( 'Premature end-of-file encountered in %s\n' % self.pbmfile )
        return False


    def loadfile( self, pbmfile, pickle_file ):
        # Deal with a missing .pbm extension
        if not os.path.exists( pbmfile ):
            if os.path.exists( pbmfile + '.pbm' ):
                pbmfile += '.pbm'
            elif os.path.exists( pbmfile + '.PBM' ):
                pbmfile += '.PBM'
        else:
            # Path exists: Do nothing
            pass

        # Open the input file
        # This may raise an exception which is fine by us
        self.pbmfile = pbmfile
        self.pickle_file = pickle_file
        f = open( self.pbmfile, 'r' )

        # Find out whether the data is raw (P4) or in ASCII (P1)
        magic_number = f.readline(4).strip() # Read just the first 4 bytes of data

        # PBM files must be P1 or P4
        if magic_number in ['P4', 'P1']:
            self.width, self.height = ( 0, 0 )
            while True:
                line = f.readline()
                if not line.startswith( '#' ):
                    self.width, self.height = tuple( map( int, line.split() ) )
                    break

            # Did we actually read anything (useful)?
            if ( self.width == 0 ) or ( self.height == 0 ):
                sys.stderr.write( 'Unable to read sensible bitmap dimensions for %s\n' % self.pbmfile )
                f.close()
                return False

            if magic_number[1] == '1':
                ok = self.__load_pbm_p1( f )


        else:
        # Unsupported file type
            sys.stderr.write( 'Input file %s is not a supported file type\n' % self.pbmfile )
            sys.stderr.write( 'Must be a PBM file or file of (x, y) coordinates\n' )
            f.close()
            return False


        # All done with the input file
        f.close()

        # If ok is False, then __load_xxx() will have printed an error
        # message already, and Python performs a sys.exit(1) on returning
        return ok


    def writecoordfile(self, coordfile):
        f = open( coordfile, 'w' )

        # And now write city coordinates to file
        f.write( '%d\n' % self.city_count )
        for i in range(0, len(self.citydict)):
            line = "{} {}\n".format(self.citydict[i][0], self.citydict[i][1])
            f.write(line)

        # And finally an EOF record
        print("\nThe image is made of ", self.city_count, "  cities\n")
        f.close()


if __name__ == '__main__':

    pbmfile, coordfile, pickle_file  = sys.argv[1:]
    city = tspCityCoord()
    if not city.loadfile( pbmfile, pickle_file ):
        sys.exit(1)

    city.writecoordfile(coordfile)
