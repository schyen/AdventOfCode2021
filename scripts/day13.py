# load modules
import argparse
from copy import deepcopy

# # set up arguments
# parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 13 puzzle')
# parser.add_argument('infile', type=str, help='data input file')
# parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

# args = parser.parse_args()

infile = "data/d13_input.txt"
puzzle = 2

# infile = args.infile
# puzzle = args.puzzle
######################################################
######################################################
# read in data
with open(infile) as file:
    dat = [] # list of tuples
    fold = [] # list of list
    for line in file:
        entry = line.rstrip()
        # fold instructions
        if "fold" in entry:
            entry = entry.replace('fold along ', '')
            entry = entry.split('=')
            entry[1] = int(entry[1])
            fold.append(entry)
        # ignore empty line
        elif entry == '':
            pass
        # point coordinates
        else:
            entry = entry.split(',')
            entry = (int(entry[0]), int(entry[1])) # put as tuple
            dat.append(entry)

# function to transpose x coordinates across the y_fold
def transpose_x(point, v_fold):
    # first need to find distance of x coordinate to y-fold
    delta = abs(point[0] - v_fold)

    # transpose factor is 2x the delta
    transpose = 2*delta

    # check is point is below y_fold
    if point[0] > v_fold:
        # transpose x coordinate
        new_x = point[0] - transpose
    else:
        new_x = point[0]

    return (new_x, point[1])

def transpose_y(point, h_fold):
    # first need to find distance of y coordinate to x-fold
    delta = abs(point[1] - h_fold)

    # transpose factor is 2x the delta
    transpose = 2*delta

    # check is point is below h_fold
    if point[1] > h_fold:
        # transpose x coordinate
        new_y = point[1] - transpose
    else:
        new_y = point[1]

    return (point[0], new_y)

# fold along y
folded = deepcopy(dat) # copy dat to new object
for n, crease in enumerate(fold):
    for i, point in enumerate(folded):
        if crease[0] == 'x':
            folded_point = transpose_x(point, crease[1])
        else:
            folded_point = transpose_y(point, crease[1])
        folded[i] = folded_point
    if puzzle == 1:
        if n == 0:
            break

# get unique points
folded = list(set(folded))

if puzzle == 1:
    answer = len(folded)
    print('answer is:')
    print(answer)

# function to plot out coordinates
def plot_coordinates(all_coord):
    # first find plot boundaries
    max_x = max([coord[0] for coord in all_coord]) + 1
    max_y = max([coord[1] for coord in all_coord]) + 1

    # initiate grid
    grid = []

    for y in range(0, max_y):
        grid_row = []
        for x in range(0, max_x):
            if (x,y) in all_coord:
                grid_row.append('#')
            else:
                grid_row.append('.')
        grid.append(grid_row)
    print(*grid, sep='\n')
    

if puzzle == 2:
    plot_coordinates(folded)