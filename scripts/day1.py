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
	dat = [line.rstrip() for line in dat]

# convert values to int
dat = list(map(int, dat))

def puzzle_one():
	print('solving puzzle 1')
	
	n_inc = 0
	for i, v in enumerate(dat):
		i_next = i + 1
		if i_next == len(dat) :
			break
		elif dat[i_next] > v:
			n_inc = n_inc + 1


	print('answer is:')
	print(n_inc)

def puzzle_two():
	print('solving puzzle 2')

	n_inc = 0
	for i, v in enumerate(dat):
		i_next = i + 1
		
		if i_next == len(dat) :
			print('end!')
			break
		else:
			window1 = sum(dat[i:i+3])
			window2 = sum(dat[i_next:i_next + 3])
			if window2 > window1:
				
				n_inc = n_inc + 1


	print('answer is:')
	print(n_inc)



if(args.puzzle == 1):
	puzzle_one()
else:
	puzzle_two()
