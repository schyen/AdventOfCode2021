# load modules
import argparse
import collections

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 6 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# class lanternfish
class Lanternfish:
    # initiate lanternfish with reproductive cycle
    def __init__(self, cycle):
        self.cycle = cycle

    # method to reduce cycle with each passing day
    def passing_day(self):
        self.cycle -= 1

#####################################################
######################################################
# read in data
with open(args.infile) as file:
    dat = file.readlines()
    dat = [line.rstrip().split(',') for line in dat]
    dat = [int(x) for x in dat[0]]

# read all fish into list of lanternfish
school = []
for f in dat:
    fish = Lanternfish(f)
    school.append(fish)

def model_lanternfish(end):

    fish_counter = 0
    for day in range(0,end):
        print(day)
        while True:
            # look at current fish
            fish = school[fish_counter]


            # a day has passed
            fish.passing_day()

            # if starting new cycle
            if fish.cycle < 0:
                # reset cycle to day 6
                fish.cycle = 6

                # create new fish
                new_fish = Lanternfish(9)

                # add new fish to school of fish
                school.append(new_fish)

            # move onto next fish
            fish_counter += 1

            # move on to next day when reached end of the school
            if fish_counter == len(school):
                # reset fish counter
                fish_counter = 0
                break
    
    return(len(school))

# modelling lanternfish not scalable
# this time count the number of fish at each age
def fish_by_age(end):
    # tally how many fish in the original school
    ## gives dictionary of age groups and number of fish at that age
    fish_tally = collections.Counter(dat)
    
    # existing age groups
    age_exist = fish_tally.keys()

    # fill out rest age groups
    add_age = [x for x in range(0,9) if x not in age_exist]
    for a in add_age:
        fish_tally[a] = 0

    # make ordered dictionary
    fish_tally = collections.OrderedDict(sorted(fish_tally.items()))

    # go through one day at a time
    for day in range(0, end):

        # current fish tally
        curr_tally = [x[1] for x in list(fish_tally.items())]
        
        # number of zeroes is the number of new fish
        n_new = fish_tally.get(0)
        
        # number of fish in each age group shifts down by one
        update = curr_tally[1:9]
        update.append(curr_tally[0])
        # number of fish at age 6 increments by number of new fish
        update[6] = update[6] + n_new

        # update values in ordered dictionary
        fish_tally.update((key, update[key]) for key in list(fish_tally.keys()))
        
    # add total number of fish
    n_fish = [x[1] for x in list(fish_tally.items())]
    return sum(n_fish)

if args.puzzle == 1:
    print('solving puzzle 1')
    answer = model_lanternfish(80)
    print('answer is:')
    print(answer)

if args.puzzle == 2:
    print('solving puzzle 2')
    answer = fish_by_age(256)
    print('answer is:')
    print(answer)