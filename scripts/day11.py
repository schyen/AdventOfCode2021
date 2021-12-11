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

# function to find coordinates adjacent values to a position
def find_adjacent(dat, coord):

    i = coord[0]
    j = coord[1]
    adjacent = []
    # looking up
    if i-1 >= 0:
        adjacent_val = dat[i-1][j]
        adjacent.append((i-1, j))
            
    # looking down
    if i+1 < len(dat):
        adjacent_val = dat[i+1][j]
        adjacent.append((i+1, j))
            
    # looking left
    if j-1 >= 0:
        adjacent_val = dat[i][j-1]
        adjacent.append((i, j-1))

    # looking right
    if j+1 < len(dat[0]):
        adjacent_val = dat[i][j+1]
        adjacent.append((i, j+1))

    # looking top left
    if i-1 >= 0 and j-1 >= 0:
        adjacent_val = dat[i-1][j-1]
        adjacent.append((i-1, j-1))
    
    # looking top right
    if i-1 >= 0 and j+1 < len(dat[0]):
        adjacent_val = dat[i-1][j+1]
        adjacent.append((i-1, j+1))

    # looking bottom left
    if i+1 < len(dat) and j-1 >= 0:
        adjacent_val = dat[i+1][j-1]
        adjacent.append((i+1, j-1))

    # looking bottom right
    if i+1 < len(dat) and j+1 < len(dat[0]):
        adjacent_val = dat[i+1][j+1]
        adjacent.append((i+1, j+1))

    return adjacent

# increment value due to nature of a step
def step_increment(dat):
    for i, row in enumerate(dat):
        for j, col in enumerate(dat[0]):
            # always increment by 1 when changing steps
            increment = 1

            # new value
            new_val = dat[i][j] + increment
            if new_val > 9:
                new_val = 0
            
            dat[i][j] = new_val
    
    return dat

# find coordinates of zeroes
def find_zero(dat):
    keep_coord = []
    for i, row in enumerate(dat):
        for j, col in enumerate(dat[0]):
            if dat[i][j] == 0:
                keep_coord.append((i,j))
    return keep_coord

# increment value due to flashes
def flash_increment(dat, zero_coord):
    # find adjacent values
    coord_adjacent = find_adjacent(dat, zero_coord)
    # increase value of adjacents by one
    for adjacent in coord_adjacent:
        i = adjacent[0]
        j = adjacent[1]

        curr_val = dat[i][j]
        if curr_val != 0:
            # new value
            new_val = dat[i][j] + 1
            if new_val > 9:
                new_val = 0
        
            dat[i][j] = new_val
    
    return dat

# count flashes
def count_flash(dat):
    n_flash = 0
    for i, row in enumerate(dat):
        # count zeroes
        n_flash += dat[i].count(0)
    return n_flash

step = 0
n_flash = 0
while True:
    # energy change due to change in step
    dat = step_increment(dat)
    # find position of zeroes
    zero_coord = find_zero(dat)

    if len(zero_coord) > 0:
        # go through one zero coordinate at a time
        iter = 0
        while True:
            # energy change due to flashes
            dat = flash_increment(dat, zero_coord[iter])

            # look for new zero
            curr_zero = find_zero(dat)

            # add new zeros of zero coord list
            new_zero = [x for x in curr_zero if x not in zero_coord] 
            zero_coord = zero_coord + new_zero

            iter += 1
            if iter == len(zero_coord):
                break

    # count how many 0s
    curr_flash = count_flash(dat)
    n_flash += curr_flash
    
    # increment step
    step += 1
    # puzzle 1
    if args.puzzle == 1:
        if step == 100:
            print('answer is:')
            print(n_flash)
            break

    # puzzle 2
    if args.puzzle == 2:
        if curr_flash == 100:
            print('answer is:')
            print(step)
            break


