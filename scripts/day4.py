# load modules
import argparse
import numpy as np

# set up arguments
parser = argparse.ArgumentParser(description='Advent of Code 2021 Day 4 puzzle')
parser.add_argument('infile', type=str, help='data input file')
parser.add_argument('--puzzle', type=int, choices=[1,2], help='solve puzzle 1 or puzzle 2')

args = parser.parse_args()

# # define iterator class
# class IterBoard:
# 	def __init__(self, board):
# 		self._board = board
# 		self._index = -1

# 	def __next__(self):
# 		self._index += 1
# 		if self._index >= len(self._board):
# 			self._index = -1
# 			raise StopIteraction
# 		else:
# 			return self._board[self._index]

# define a bingo board class
class BingoBoard:

	# # return iterator object to make class iterable
	# def __iter__(self):
	# 	return IterBoard(self)

	# initialize board as array
	def __init__(self, data):
		self.winner = False
		self.board = np.array(data)
		# initiate marker board
		self.marker = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
		self.unmarked = np.array(data)

	# method to check if board is winning
	def check_winner(self):
		row_sum = self.marker.sum(axis=1)
		col_sum = self.marker.sum(axis=0)
		# put row and col sums in one list
		board_summary = [list(row_sum), list(col_sum)]
		# flatten list of list
		board_summary = [x for sublist in board_summary for x in sublist]
		if any(x == 5 for x in board_summary):
			self.winner = True
		else:
			self.winner = False

	# method to mark board
	def mark_board(self, draw):
		# check if draw is on the board
		if draw in self.board:
			# mark marker board based on index of drawn number
			mark_pos = np.where(self.board == draw)
			self.marker[mark_pos] = 1

	# method to get unmarked numbers
	def get_unmarked(self):
		unmarked_pos = np.where(self.marker == 0)
		out = self.unmarked[unmarked_pos]

		return(list(out))

# read in data
with open(args.infile) as file:
	# read in first line as draw pool
	draw_pool = file.readline().strip()

	# read in remaining lines to separate boards later
	raw = file.readlines()
	raw = [line.rstrip() for line in raw]

# convert draw pool to list of int
draw_pool = draw_pool.split(',')
draw_pool = list(map(int, draw_pool))
print(draw_pool)

# initialize list of boards
boards = []

# go through raw one line at a time
# initialize first entry
entry = []
counter = 0
for line in raw:
	# do nothing first iteration
	if counter == 0:
		counter += 1
		continue
	# when encounter empty line, initialize new board
	if line == '':
		# add board entry
		boards.append(entry)
		# reset entry
		entry = []

	# build board entry
	else:
		# convert line into list of integers
		line_list = line.split(' ')
		# check drop empty values
		line_list = [x for x in line_list if x != '']
		line_list = list(map(int, line_list))
		entry.append(line_list)

# add last board
boards.append(entry)

# list of bingoboards
game = []
for b in boards:
	entry = BingoBoard(b)
	game.append(entry)


if args.puzzle == 1:
	print('solving puzzle 1')

	found_winner = False
	# go through one draw at a time
	for draw in draw_pool:
		# feed draw into each board
		for b in game:

			# mark bingo board
			b.mark_board(draw)
			
			# check if board is winner
			b.check_winner()


			if b.winner:
				print('found winner')
				unmarked_sum = sum(b.get_unmarked())
				found_winner = True
				break
			
		if found_winner:
			break

	answer = unmarked_sum * draw
	print(answer)

if args.puzzle == 2:
	print('solving puzzle 2')

	winning_boards = []
	# go through one draw at a time
	for draw in draw_pool:
		# feed draw into each board
		for i, b in enumerate(game):

			# mark bingo board
			b.mark_board(draw)
			
			# check if board is winner
			b.check_winner()

			# track index of winning board
			if b.winner:
				if i not in winning_boards:
					winning_boards.append(i)

				if len(winning_boards) == len(game):
					print('last board completed')
					unmarked_sum = sum(b.get_unmarked())
					break
			
		if len(winning_boards) == len(game):
			break

	answer = unmarked_sum * draw
	print(answer)
