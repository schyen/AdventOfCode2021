# load modules
import argparse
from collections import Counter
import timeit

# # set up arguments
# parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 13 puzzle')
# parser.add_argument('infile', type=str, help='data input file')
# parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

# args = parser.parse_args()

infile = "data/d14_input.txt"
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
    stop = timeit.default_timer()
    print('Time: ', stop - start)

# how long will the polymer be after 40 steps
def polymer_length(n, step=0):
    if step == 40:
        return n
    else:
        step = step + 1
        n = (n - 1) + n
        return polymer_length(n, step)

if puzzle == 0:
    poly_len = polymer_length(4, 0)
    print(poly_len) # 3.2 trillion :(

# solution not scalable. try new approach for puzzle 2.
# it's ten times faster!

# function to identify monomers to insert and the number of times to insert them
def indentify_insert(pair_tally):
    insert_tally = Counter({})
    for pair in pair_tally.keys():
        insert = rules.get(pair)
        if insert_tally.get(insert) is None:
            insert_tally[insert] = pair_tally.get(pair)
        else:
            insert_tally[insert] = insert_tally.get(insert) + pair_tally.get(pair)
    return insert_tally

# function to build new set of pairs from pairs tally
def build_pairs(pair_tally):
    new_pairs = Counter({})
    for pair in pair_tally.keys():
        # find corresponding insertion
        insert = rules.get(pair)
        one = pair[0] + insert
        two = insert + pair[1]
        if new_pairs.get(one) is None:
            new_pairs[one] = pair_tally.get(pair)
        else:
            new_pairs[one] = new_pairs.get(one) + pair_tally.get(pair)
        if new_pairs.get(two) is None:
            new_pairs[two] = pair_tally.get(pair)
        else:
            new_pairs[two] = new_pairs.get(two) + pair_tally.get(pair)

    return new_pairs

if puzzle == 2:
    start = timeit.default_timer()
    # first find pairs in template
    pairs = locate_pairs(template) # [NN, NC, CH]
    pair_tally = Counter(pairs) # [NN:1, NC:1, CH:1]

    # initiate counter of template
    monomer_count = Counter(template) # [N:2, C:1, H1]

    for step in range(0,40):
        # identify monomers to be inserted
        insert_tally = indentify_insert(pair_tally) # [B:1, C:1, H:1]

        # update counter
        monomer_count = monomer_count + insert_tally

        # build new pair tally
        pair_tally = build_pairs(pair_tally) # [NB:1, BN:1, NC:1, CC:1, CH:1, HH:1]

    monomer_order = monomer_count.most_common()
    # get most and least common monomer
    max_monomer = monomer_order[0][1]
    min_monomer = monomer_order[-1][1]

    answer = max_monomer - min_monomer

    stop = timeit.default_timer()
    print('answer is:')
    print(answer)
    print('Time: ', stop - start) 