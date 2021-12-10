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
class chunk():
    def __init__(self, bracket):
        self.bracket = bracket
        if bracket in ['(','[','<','{']:
            self.status = 'open_chunk'
            self.type = 'open_bracket'
        else:
            self.type= 'closed_bracket'
        if bracket in ['(',')']:
            self.style = 'round'
        elif bracket in ['[',']']:
            self.style = 'square'
        elif bracket in ['{','}']:
            self.style = 'curly'
        else:
            self.style = 'angle'

    # method to 
######################################################
######################################################
# read in data
with open(args.infile) as file:
    dat = file.readlines()
    dat = [line.rstrip() for line in dat]

corrupting_chunks = []
correction = []
# go through one line at a time
for line in dat:
    # initiate list of open chunks
    open_chunks = []
    line_correction = []
    # initiate line diagnosis
    line_diagnosis = None
    # step through each bracket in the line
    for bracket in line:
        # assign bracket as a chunk class
        curr_chunk = chunk(bracket)
        # if open bracket add it to list of open brackets
        if curr_chunk.type == 'open_bracket':
            open_chunks.append(curr_chunk)
        # compare closed bracket with most recent open bracket
        else:
            # if bracket style matches most recent open chunk
            if curr_chunk.style == open_chunks[-1].style:
                # assign status as closed_chunk
                open_chunks[-1].status = 'closed_chunk'
                # drop closed_chunk from list
                del open_chunks[-1]
            # if bracket style does not match diagnose line as corrupt
            else:
                line_diagnosis = 'corrupt' 
                # record corrupting bracket
                corrupting_chunks.append(curr_chunk)
                # stop going through the current line
                break
    # if line diagnosis is unchanged and still open chunks left mark as incomplete
    if line_diagnosis is None and len(open_chunks) > 0:
        line_diagnosis = 'incomplete'
        
        # go through the remaining open chunks
        for open_chunk in open_chunks:
            # use chunk style to know how to correct open chunk
            line_correction.append(open_chunk)

    # store line correction for later use
    if line_diagnosis == 'incomplete':
        correction.append(list(reversed(line_correction)))

if args.puzzle == 1:
    print('solving puzzle 1')
    # look at bracket style of corrupting chunks
    score = []
    for corrupt in corrupting_chunks:
        if corrupt.style == 'round':
            entry = 3
        elif corrupt.style == 'square':
            entry = 57
        elif corrupt.style == 'curly':
            entry = 1197
        else:
            entry = 25137
        score.append(entry)

    answer = reduce(lambda x, y: x+y, score)

    print('answer is:')
    print(answer)

if args.puzzle == 2:
    print('solving puzzle 2')

    # calculate score for one line at a time
    score = []
    for line in correction:
        line_score = 0
        for correcting_chunk in line:
            if correcting_chunk.style == 'round':
                addition = 1
            elif correcting_chunk.style == 'square':
                addition = 2
            elif correcting_chunk.style == 'curly':
                addition = 3
            else:
                addition = 4
            line_score = line_score * 5 + addition
        score.append(line_score)

    score = sorted(score)
    ind = (len(score) - 1) / 2
    answer = score[int(ind)]
    
    print('answer is:')
    print(answer)