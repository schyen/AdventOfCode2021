# load modules
import argparse
from collections import Counter

# # set up arguments
# parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 13 puzzle')
# parser.add_argument('infile', type=str, help='data input file')
# parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

# args = parser.parse_args()

infile = "data/d14_test.txt"
puzzle = 2

# infile = args.infile
# puzzle = args.puzzle
######################################################
######################################################
# read in data
with open(infile) as file:
    rules = {} # dictionary where pairs are key and insertion is value
    for line in file:
        entry = line.rstrip()
        # pair insertion rule
        if "->" in entry:
            entry = entry.split(' -> ')
            rules[entry[0]] = entry[1]
        # ignore empty line
        elif entry == '':
            pass
        # point coordinates
        else:
            template = entry # starting template

# function to extract pairs in template and their index locations
def locate_pairs(template):
    pairs = [] # list of [index, pair]
    for ind in range(0, len(template)-1):
        curr_pair = template[ind] + template[ind+1]
        entry = [ind, curr_pair]
        pairs.append(entry)
    return pairs

# function to perform the polymer insertion -- acts on one pair at a time
def insert_polymer(pair):
    inserted = pair[1][0] + rules.get(pair[1]) + pair[1][1]
    
    return inserted

# function to stitch together polymer fragments
def stitch_polymer(fragments):
    polymer = ''
    for i, fragment in enumerate(fragments):
        if i < (len(fragments) - 1):
            # drop last letter in fragment
            entry = fragment[0:-1]
        else:
            entry = fragment
        polymer = polymer + entry 
    
    return polymer

# putting functions together for one step
def extend_polymer(template):
    # first locate pairs in template
    pairs = locate_pairs(template)

    # make polymer fragments
    fragments = []
    for pair in pairs:
        fragment = insert_polymer(pair)
        fragments.append(fragment)

    # stitch together fragments
    polymer = stitch_polymer(fragments)

    return polymer

###### puzzle 1 #############
if puzzle == 1:
    last_step = 10
else:
    last_step = 40

for step in range(0,last_step):
    print(step)
    template = extend_polymer(template)

polymer = template
# count occurance of each monomer
monomer_tally = Counter(polymer).most_common()

# get most and least common monomer
max_monomer = monomer_tally[0][1]
min_monomer = monomer_tally[-1][1]

answer = max_monomer - min_monomer
print('answer is:')
print(answer)