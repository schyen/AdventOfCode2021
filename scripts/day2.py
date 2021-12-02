# Advent of code 2021 Day 1 

# load modules
import argparse

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 1 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# read in input
with open(args.infile) as file:
	dat = file.readlines()
	dat = [line.rstrip().split() for line in dat]

def puzzle_one():

	# order of instructions don't matter
	# separating movements by direction
	h_move = [x for x in dat if x[0] == 'forward']
	d_inc = [x for x  in dat if x[0] == 'down']
	d_dec = [x for x in dat if x[0] == 'up']

	h_pos = sum([int(x[1]) for x in h_move])
	inc_move = sum(int(x[1]) for x in d_inc)
	dec_move = sum(int(x[1]) for x in d_dec)

	d_pos = inc_move - dec_move

	answer = h_pos * d_pos
	print("answer is:")
	print(answer)


def puzzle_two():

	# instructions must be done in order
	h_pos = 0
	d_pos = 0
	aim = 0

	for t in dat:
		if t[0] == 'forward':
			h_pos = h_pos + int(t[1])
			d_pos = d_pos + (int(t[1]) * aim)
		elif t[0] == 'up':
			aim = aim - int(t[1])
		elif t[0] == 'down':
			aim = aim + int(t[1])

	answer = h_pos * d_pos
	print("answer is:")
	print(answer)


if(args.puzzle == 1):
	puzzle_one()
else:
	puzzle_two()
