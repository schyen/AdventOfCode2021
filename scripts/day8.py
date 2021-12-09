# load modules
from collections import Counter

# load modules
import argparse
from collections import Counter

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 8 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# define reference segement
ref = {0 : 'abcefg', 1 : 'cf', 2 : 'acdeg', 3 : 'acdfg', 4 : 'bcdf', 5 : 'abdfg', 6 : 'abdefg', 7 : 'acf', 8 : 'abcdefg', 9 : 'abcdfg'}

# version of reference dictionary showing number of segments
ref_n = {}
for key in ref.keys():
    val = ref.get(key)
    entry = len(val)
    ref_n[key] = entry

# find digits with unique number of segments
unique_seg_n = Counter(ref_n.values())
unique_seg_n = [item[0] for item in unique_seg_n.items() if item[1] == 1]
unique_seg_n = [item[0] for item in ref_n.items() if item[1] in unique_seg_n]

unique_seg = [ref.get(x) for x in unique_seg_n]

######################################################
######################################################
# read in data
reading = []
display = []
with open(args.infile) as file:
    # separate out digit output from digit readings
    for line in file:
        raw = line.rstrip().split(' | ')
        entry_reading = raw[0].split(' ')
        entry_display = raw[1].split(' ')
        # sort in alphabetical order
        entry_reading = [''.join(sorted(x)) for x in entry_reading]
        entry_display = [''.join(sorted(x)) for x in entry_display]
        reading.append(entry_reading)
        display.append(entry_display)

# map numbers based on unique number of segments
def map_by_n(four_digit, target):

    # are length of segments in digits
    length = [len(x) for x in four_digit]
    target_length = [len(x) for x in target]
    boolean = [x in target_length for x in length]

    return sum(boolean)

# map_seg for one, four, seven, eight
def map_seg_init(ten_digit):
    # length of segements in digits
    length = [[x, len(x)] for x in ten_digit]
    # extract values for 1,4,7,8
    one = [x[0] for x in length if x[1] == 2][0]
    four = [x[0] for x in length if x[1] == 4][0]
    seven = [x[0] for x in length if x[1] == 3][0]
    eight = [x[0] for x in length if x[1] == 7][0]
    # populate map with unique segments
    map_seg = {1:one, 4:four, 7:seven, 8:eight}
    return map_seg

# use map of segements to translate digits with 5 segements (2,3,5)
def map_five_seg(map_seg, query):
    # get letters used in 1, 4, 7
    ref = [v for k, v in map_seg.items() if k in [1,4,7]]
    ref = ''.join(ref)
    ref = list(set(ref))
    # map 2
    for q in query:
        diff = [x for x in q if x not in ref]
        if len(diff) == 2:
            # add 2 to dictionary
            map_seg[2] = q 
            # drop q from query
            query = [x for x in query if x != q]
    ref = [v for k, v in map_seg.items() if k in [1,2,7]]
    ref = ''.join(ref)
    ref = list(set(ref))
    # map 5 and 3
    for q in query:
        diff = [x for x in q if x not in ref]
        if len(diff) == 1:
            # add 5 to dictionary
            map_seg[5] = q
        else:
            map_seg[3] = q
    return map_seg

# use map of segments to translate digits with 6 segments (0,6,9)
def map_six_seg(map_seg, query):
    # letters for 5,4
    ref = [v for k, v in map_seg.items() if k in [5,4]]
    ref = ''.join(ref)
    ref = list(set(ref))
    for q in query:
        diff = [x for x in q if x not in ref]
        # map 9
        if len(diff) == 0:
            map_seg[9] = q
            # drop q from query
            query = [x for x in query if x != q]
    ref = map_seg.get(7)
    for q in query:
        extra_ref = [x for x in ref if x not in q]
        if len(extra_ref) == 1:
            map_seg[6] = q
        elif len(extra_ref) == 0:
            map_seg[0] = q
    return map_seg

# use map_seg to translate four-digit
def map_four_digit(map_seg, four_digit):
    out = []
    for d in four_digit:
        entry = [k for k,v in map_seg.items() if v == d]

        out.append(entry[0])
    return(out)

if args.puzzle == 1:
    print('solving puzzle 1')
    # go through four-digit displays
    n_found = 0
    for four_digit in display:
        curr_found = map_by_n(four_digit, unique_seg)
        n_found = n_found + curr_found

    print('answer is:')
    print(n_found)

if args.puzzle == 2:
    print('solving puzzle 2')
    display_sum = 0
    for i, ten_digit in enumerate(reading):

        # initialize map
        map_seg = map_seg_init(ten_digit)
        # identify digits with 5 segments
        five_seg = [d for d in ten_digit if len(d) == 5]
        six_seg = [d for d in ten_digit if len(d) == 6]
        # cross reference five-seg digits with segment map
        map_seg = map_five_seg(map_seg, five_seg)
        map_seg = map_six_seg(map_seg, six_seg)

        # translate four-digit
        curr_display = map_four_digit(map_seg, display[i])
        curr_display = int(''.join(map(str,curr_display)))

        display_sum = display_sum + curr_display

    answer = display_sum
    print('answer is')
    print(answer)