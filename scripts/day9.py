# load modules
import argparse
from functools import reduce

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 6 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

######################################################
######################################################
# read in data
with open(args.infile) as file:
    dat = []
    for line in file:
        line = line.rstrip()
        entry = [val for val in line]
        entry = [int(x) for x in entry]
        dat.append(entry)
## input is list of lists -- each row in a list

# specify start and end point
first_row = 0
first_col = 0
last_row = len(dat)-1
last_col = len(dat[0])-1

# nested loop to move through every pos
low_point = []
low_coord = []
for i, row in enumerate(dat):
    for j, col in enumerate(row):
        # current value
        curr_val = dat[i][j]

        # define adjacent values
        if i == first_row:
            u_val = float('inf')
        else:
            u_val = dat[i-1][j]

        if i == last_row:
            d_val = float('inf')
        else:
            d_val = dat[i+1][j]
        
        if j == first_col:
            l_val = float('inf')
        else:        
            l_val = dat[i][j-1]
        
        if j == last_col:
            r_val = float('inf')
        else:
            r_val = dat[i][j+1]

        adjacent = [u_val, d_val, l_val, r_val]
        if all([curr_val < x for x in adjacent]):
            low_point.append(curr_val)
            low_coord.append((i,j))

def compare_adjacent(dat, coord, direction):
    # specify start and end point
    first_row = 0
    first_col = 0
    last_row = len(dat)-1
    last_col = len(dat[0])-1

    i = coord[0]
    j = coord[1]

    keep_coord = []

    while True:
        # looking up
        if direction == 'up':
            if i == first_row:
                break
            adjacent_val = dat[i-1][j]
            if adjacent_val < 9:
                keep_coord.append((i-1,j))
            else:
                break
            # increment position
            i += -1
        
        # looking down
        if direction == 'down':
            if i == last_row:
                break
            adjacent_val = dat[i+1][j]
            if adjacent_val < 9:
                keep_coord.append((i+1,j))
            else:
                break
            # increment position
            i += 1

        # looking left
        if direction == 'left':
            if j == first_col:
                break
            adjacent_val = dat[i][j-1]
            if adjacent_val < 9:
                keep_coord.append((i,j-1))
            else:
                break
            # increment position
            j += -1
        
        # looking right
        if direction == 'right':
            if j == last_col:
                break
            adjacent_val = dat[i][j+1]
            if adjacent_val < 9:
                keep_coord.append((i, j+1))
            else:
                break
            # increment position
            j += 1

    return keep_coord



# puzzle 1: find low points
if args.puzzle == 1:
    risk = [x + 1 for x in low_point]
    answer = sum(risk)
    print('answer is;')
    print(answer)

# puzzle 2: find decreasing points
if args.puzzle == 2:
    # this time put surrounding land to negative infinity
    # go through low points and keep increasing values
    basin_size = []
    for basin in low_coord:
        keep_looking = True
        basin_coord = [basin]
        i = 0
        while keep_looking:
            up = compare_adjacent(dat, basin_coord[i], 'up')
            down = compare_adjacent(dat, basin_coord[i], 'down')
            left = compare_adjacent(dat, basin_coord[i], 'left')
            right = compare_adjacent(dat, basin_coord[i], 'right')
            found = []
            if len(up) > 0:
                found = found + up
            if len(down) > 0:
                found = found + down
            if len(left) > 0:
                found = found + left
            if len(right) > 0:
                found = found + right
            if len(found) > 0:
                found = set(found)
                new = [x for x in found if x not in basin_coord]
            else:
                new = []

            if len(new) > 0: 
                for x in new:
                    basin_coord.append(x)
            i += 1
            if i == len(basin_coord):
                keep_looking = False
            
        basin_size.append(len(basin_coord))
    
    answer = sorted(basin_size)[-3:]
    answer = reduce(lambda x, y: x*y, answer)
    print('answer is')
    print(answer)
    
    
