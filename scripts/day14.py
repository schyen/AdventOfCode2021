# load modules
import argparse
from collections import Counter
import timeit

# # set up arguments
# parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 13 puzzle')
# parser.add_argument('infile', type=str, help='data input file')
# parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

# args = parser.parse_args()

infile = "data/d14_test.txt"
puzzle = 0

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
    pairs = []
    for ind in range(0, len(template)-1):
        entry = template[ind] + template[ind+1]
        pairs.append(entry)
    return pairs

# function to perform the polymer insertion -- acts on one pair at a time
def insert_polymer(pair):
    inserted = pair[0] + rules.get(pair) + pair[1]
    
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
    start = timeit.default_timer()
    for step in range(0,10):
        print(step)
        template = extend_polymer(template)

    polymer = template
    # count occurance of each monomer
    monomer_tally = Counter(polymer).most_common()

    # get most and least common monomer
    max_monomer = monomer_tally[0][1]
    min_monomer = monomer_tally[-1][1]

    answer = max_monomer - min_monomer

    stop = timeit.default_timer()
    print('answer is:')
    print(answer)
    print('Time: ', stop - start)

# how long will the polymer be after 40 steps
def polymer_length(n, step=0):
    if step == 40:
        return n
    else:
        step = step + 1
        n = (n - 1) + n
        return polymer_length(n, step)
poly_len = polymer_length(4, 0)
print(poly_len) # 3.2 trillion :(

# solution not scalable. try new approach for puzzle 2.