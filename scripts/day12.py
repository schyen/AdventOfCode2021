# load modules
import argparse
from copy import deepcopy
from collections import Counter

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 12 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# infile = "data/d12_test1.txt"
# puzzle = 2

infile = args.infile
puzzle = args.puzzle
######################################################
######################################################
# read in data
with open(infile) as file:
    dat = []
    cave_list = []
    for line in file:
        entry = line.rstrip().split('-')
        cave_entry = [x for x in entry if x not in cave_list]
        cave_list = cave_list + cave_entry
        dat.append(entry)
## input is list of lists

# define class Cave to store info about a cave
class Cave:
    def __init__(self, name):
        self.name = name
        self.connect = []
        if all([x.isupper() for x in name]):
            self.size = 'big'
        else:
            self.size = 'small'

    def connecting_caves(self, pair):
        entry = [x for x in pair if x != self.name]
        if entry not in self.connect:        
            self.connect = self.connect + entry

class Path:
    # cave order is list of Caves
    def __init__(self, first_cave):
        self.cave_order = [first_cave]
        self.complete = False

    def is_complete(self):
        if self.last_cave().name == 'end':
            self.complete = True

    # adding cave to path
    def add_cave(self, cave):
        self.cave_order.append(cave)
        
    # remove last cave
    def pop_cave(self):
        self.cave_order.pop()

    # retrieving name of caves in path
    def show_path(self):
        cave_name = []
        for cave in self.cave_order:
            cave_name.append(cave.name)
        return cave_name

    # retrieving last cave in path
    def last_cave(self):
        return self.cave_order[-1] 

    # generate path id based on cave order
    def get_id(self):
        id = ''.join(self.show_path())
        return(id)

# check if candidate caves and returns valid caves
def valid_cave(path, candidate):
    out = []
    # need to check if a cave can be added to an existing path
    for cave in candidate:
        # if candidate is a small cave, it must not be part of path
        if cave.size == 'small':
            if cave.name not in path.show_path():
                out.append(cave)
        # if candidate is a large cave, can add directly to path
        else:
            out.append(cave)
    return out

# check if candidate caves and returns valid caves
def valid_cave2(path, candidate):
    out = []
    # check how many times small caves have been visited in path
    small_tally = Counter([x.name for x in path.cave_order if x.size == 'small'])
    
    # need to check if a cave can be added to an existing path
    for cave in candidate: 
        go_again = all([x == 1 for x in small_tally.values()])
        if cave.name in ['start','end']:
            go_again = False
        # if candidate is a small cave, it must not be part of path
        if cave.size == 'small':
            if (cave.name not in path.show_path()) or (go_again):
                out.append(cave)
        # if candidate is a large cave, can add directly to path
        else:
            out.append(cave)
    return out

# put caves as class Cave
cave_system = [Cave(x) for x in cave_list]

# get connecting caves for each cave
for cave in cave_system:
    # get cave pairs with current cave
    pairs = []
    for pair in dat:
        if any([x == cave.name for x in pair]):
            pairs.append(pair)
    # find connecting caves
    for pair in pairs:
        cave.connecting_caves(pair)

# build list of paths;
# initiate first path with start cave
start_cave = [cave for cave in cave_system if cave.name == 'start'][0]
path_list = [Path(start_cave)]

path_ind = 0
while True:
    # current path
    curr_path = path_list[path_ind]
    # check if path is complete
    curr_path.is_complete()

    # only work on incomplete paths
    if curr_path.complete is False:
        # current cave is the last cave in connecting path
        curr_cave = curr_path.last_cave()
        
        # get connecting caves to most recent cave
        candidate_caves = [cave for cave in cave_system if cave.name in curr_cave.connect]
        if puzzle == 1:
            connecting_caves = valid_cave(curr_path, candidate_caves)
        if puzzle == 2: ## this to 2 days to run so not a great solution
            connecting_caves = valid_cave2(curr_path, candidate_caves)
        
        # for each connecting path, initiate new path
        for i, connection in enumerate(connecting_caves):
            # copy over current path -- need deepcopy
            new_path = deepcopy(path_list[path_ind])

            # add new cave
            new_path.add_cave(connection)

            # check that path is a new path
            is_new = new_path.get_id() not in [p.get_id() for p in path_list]
            
            if is_new:
                # add path to list of paths
                path_list.append(new_path)

            check = len(path_list) % 100
            if check == 0:
                print(len(path_list))
        
    # move onto next path
    path_ind += 1

    # break out when reach end of all possible paths
    if path_ind == len(path_list):        
        break

# only keep completed paths
path_list = [p for p in path_list if p.complete]
answer = len(path_list)
print('answer is:')
print(answer)
