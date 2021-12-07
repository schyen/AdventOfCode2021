# load modules
import argparse
from collections import Counter

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 6 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

#####################################################
######################################################
# read in data
with open(args.infile) as file:
    dat = file.readlines()
    dat = [line.rstrip().split(',') for line in dat]
    dat = [int(x) for x in dat[0]]

max_x = max(dat)
min_x = min(dat)

span = max_x - min_x

# find the most frequent position
pos_tally = Counter(dat)

# order positions from most to least frequent positions
freq_pos = pos_tally.most_common(len(pos_tally.keys()))

# find how much fuel it costs to get to that position
def add_fuel(dat, target):
    # initialize total fuel
    total_fuel = 0
    for crab in dat:
        curr_usage = crab - target
        total_fuel = total_fuel + abs(curr_usage)

    return total_fuel

def compound_fuel(dat, target):
    # initialize total fuel
    total_fuel = 0
    for crab in dat:
        n_increment = abs(crab - target)
        increment = 0
        curr_usage = 0
        for step in range(0, n_increment):
            increment += 1
            curr_usage = curr_usage + increment
        total_fuel = total_fuel + curr_usage

    return total_fuel

if args.puzzle == 1:
    print('solving puzzle 1')

    # try every position, starting from most frequent position
    ordered_pos = [x[0] for x in freq_pos]
    final_usage = float('inf')
    for pos in ordered_pos:
        curr_fuel = add_fuel(dat, pos)
        if(curr_fuel < final_usage):
            final_usage = curr_fuel

    answer = final_usage
    print('answer is:')
    print(answer)

if args.puzzle == 2:
    print('solving puzzle 2')

    # try every position
    final_usage = float('inf')
    for pos in range(0,span):
        curr_fuel = compound_fuel(dat, pos)
        if(curr_fuel < final_usage):
            optimal_pos = pos
            final_usage = curr_fuel

    answer = final_usage
    print(optimal_pos)

    print('answer is:')
    print(answer)