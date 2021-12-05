# load modules
import argparse
import numpy as np

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 5 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# my brain read hyperthermic vents and said volcano
# define volcano class
class Volcano:

    # initialize input data as list of coordinates [[x1,y1],[x2,y2]]
    def __init__(self, data):
        self.data = data
        self.coord1 = data[0]
        self.coord2 = data[1]

    # method to get orientation of volcano line
    def get_orientation(self):
        sorted_coord = sorted(self.data)
        if self.coord1[0] == self.coord2[0]:
            self.orientation = 'h'
        elif self.coord1[1] == self.coord2[1]:
            self.orientation = 'v'
        elif sorted_coord[0][1] > sorted_coord[1][1]:
            self.orientation = 'inc'
        elif sorted_coord[0][1] < sorted_coord[1][1]:
            self.orientation = 'dec'

# define landscape class
class Landscape:

    # initiate array based on max coord
    def __init__(self, max_x, max_y):
        grid = np.empty(shape=(max_x+1, max_y+1))
        grid.fill(0)
        self.grid = grid

    # method to update grid -- coord1 = [x1,y1], coord2 = [x2,y2]]
    def update_grid(self, coord1, coord2, orientation):
        # build index array based on coordinates
        if orientation == 'h': # horizontal
            # sort coordinates
            s = sorted([coord1[1], coord2[1]])
            l = range(s[0],s[1]+1)
            col_array = np.repeat(coord1[0], len(l))
            row_array = np.array(l)
        if orientation == 'v': # vertical
            s = sorted([coord1[0], coord2[0]])
            l = range(s[0],s[1]+1)
            col_array = np.array(l)
            row_array = np.repeat(coord1[1], len(l))
        if orientation == 'inc': # increasing diagonal
            sorted_coord = sorted([coord1, coord2])
            row = range(sorted_coord[0][0], sorted_coord[1][0] + 1)
            col = list(reversed(range(sorted_coord[1][1], sorted_coord[0][1] + 1)))
            row_array = np.array(row)
            col_array = np.array(col)
        if orientation == 'dec': # decreasing diagonal
            sorted_coord = sorted([coord1, coord2])
            row = range(sorted_coord[0][0], sorted_coord[1][0] + 1)
            col = range(sorted_coord[0][1], sorted_coord[1][1] + 1)
            row_array = np.array(row)
            col_array = np.array(col)
        # coordinates as index of grid array
        ind_array = (row_array, col_array)
        self.grid[ind_array] = self.grid[ind_array] + 1
        

######################################################
######################################################
# read in data
with open(args.infile) as file:
    dat = []
    max_x = 0
    max_y = 0
    for line in file:
        # format input data
        entry = line.rstrip()
        entry = entry.split(" -> ")
        # coordinates as list of lists [[x1,y1],[x2,y2]]
        entry = [x.split(",") for x in entry]
        # convert str to int
        entry = [[int(x[0]), int(x[1])] for x in entry]

        # check current coordinates contain max x or y
        curr_max_x = max(entry[0][0], entry[1][0])
        if curr_max_x > max_x:
            max_x = curr_max_x
        curr_max_y = max(entry[0][1], entry[1][1])
        if curr_max_y > max_y:
            max_y = curr_max_y

        # record current entry
        dat.append(entry)

# get list of volcanos
all_volcano = []
hv_volcano = []
for v in dat:
    curr_volcano = Volcano(v) # make volcano class
    curr_volcano.get_orientation() # calculate orientation
    all_volcano.append(curr_volcano)

    # separate horizontal and vertical volcanoes
    if(curr_volcano.orientation in ['h','v']):
        hv_volcano.append(curr_volcano)

# initiate landscape grid
landscape = Landscape(max_x, max_y)

if args.puzzle == 1:
    print('solving puzzle 1')
    # mark horizontal and vertical volcanoes on landscape
    for v in hv_volcano:
        landscape.update_grid(v.coord1, v.coord2, v.orientation)

    # extract values where grid > 1
    danger_ind = np.where(landscape.grid > 1)
    answer = len(landscape.grid[danger_ind])

    print('answer is:')
    print(answer)

if args.puzzle == 2:
    print('solving puzzle 2')
    # mark horizontal and vertical volcanoes on landscape
    for v in all_volcano:
        landscape.update_grid(v.coord1, v.coord2, v.orientation)

    # extract values where grid > 1
    danger_ind = np.where(landscape.grid > 1)
    answer = len(landscape.grid[danger_ind])

    print('answer is:')
    print(answer)