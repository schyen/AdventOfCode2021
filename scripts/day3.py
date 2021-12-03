# Advent of code 2021 Day 1 

# load modules
import argparse
from collections import Counter

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 1 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# read in input
with open(args.infile) as file:
	dat = file.readlines()
	dat = [line.rstrip() for line in dat]
	# input is list of lists
	dat = [list(map(int, str(x))) for x in dat]

# define class diagnostics
class Diagnositic:

	report = 'diagnostics'

	def __init__(self, data):
		self.data = data

	# function tally bits
	def count_bits(self, indat, ind, max=True, ties=None):
		# get items by index in list
		x = [b[ind] for b in indat]
		x_tally = Counter(x)

		if max:
			# most common
			out = x_tally.most_common(1)[0][0]
		else:
			# second most common (aka least common)
			out = x_tally.most_common(2)[1][0]

		if ties is not None:
			n_zero = x_tally[0]
			n_one = x_tally[1]
			if n_zero == n_one:
				out = ties
		return out

	def gamma_rate(self):
		# tally each bit position
		binary_list = []
		for i, v in enumerate(self.data[0]):
			entry = self.count_bits(self.data, i, max=True)
			binary_list.append(entry)

		binary = int(''.join(map(str, binary_list)))
		decimal = int(str(binary), 2)

		return decimal


	def episilon_rate(self):
		# tally each bit position
		binary_list = []
		for i, v in enumerate(self.data[0]):
			entry = self.count_bits(self.data, i, max=False)
			binary_list.append(entry)

		binary = int(''.join(map(str, binary_list)))
		decimal = int(str(binary), 2)

		return decimal

	def oxygen_rate(self):

		# copy input data into working data
		working_data = self.data

		# record position
		bit_pos = 0

		# continue until one value left
		while len(working_data) >= 1:
			# find most common bit
			keep_bit = self.count_bits(working_data, bit_pos, max=True, ties=1)
			# lists with correct bit in current position
			keep = [k for k in working_data if k[bit_pos] == keep_bit]
			# increment bit position
			bit_pos += 1

			# update working_data
			working_data = keep

			if len(working_data) == 1:
				break

		binary = int(''.join(map(str, working_data[0])))
		decimal = int(str(binary), 2)
		
		return decimal


	def co2_rate(self):

		# copy input data into working data
		working_data = self.data

		# record position
		bit_pos = 0

		# continue until one value left
		while len(working_data) >= 1:
			# find most common bit
			keep_bit = self.count_bits(working_data, bit_pos, max=False, ties=0)
			# lists with correct bit in current position
			keep = [k for k in working_data if k[bit_pos] == keep_bit]
			# increment bit position
			bit_pos += 1

			# update working_data
			working_data = keep

			if len(working_data) == 1:
				break

		binary = int(''.join(map(str, working_data[0])))
		decimal = int(str(binary), 2)
		
		return decimal

# puzzle 1
if args.puzzle == 1:
	print('solving puzzle 1')
	diag_report = Diagnositic(dat)

	answer = diag_report.gamma_rate() * diag_report.episilon_rate()
	print('answer is:')
	print(answer)

# puzzle 2
if args.puzzle == 2:
	print('solving puzzle 2')
	
	diag_report = Diagnositic(dat)
	
	answer = diag_report.oxygen_rate() * diag_report.co2_rate()
	print('answer is:')
	print(answer)