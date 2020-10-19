from z3 import *
import random
from functools import reduce
from itertools import *


NUM_COLS = 8
NUM_PEGS = 4
NUM_TURNS = 16

matrix = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(NUM_COLS) ]
	  for i in range(NUM_PEGS) ]

print(matrix)


def basicConstraints():

	cells_c = [ And(0 <= matrix[i][j] , matrix[i][j] <=1) for j in range(NUM_COLS) 
	  for i in range(NUM_PEGS) ]
	row_c = [And( sum(i) == 1) for i in matrix]
	return cells_c + row_c



def calcGuess(m):
	guess = []
	for i in range(NUM_PEGS):
		for j in range(NUM_COLS):
			if m[i][j] == 1:
				guess.append(j+1)
	print("guess===" , guess)
	return guess


def redWhiteCount(m , secret , guess):

	print(len(secret) , len(guess))
	red_c = 0
	white_c = 0
	for i in range(NUM_PEGS):
		if guess[i] == secret[i]:
			red_c += 1
			secret[i] = -1

	for i in range(NUM_PEGS):
		for j in range(NUM_PEGS):
			if guess[i] == secret[j]:
				white_c += 1
				secret[j] = -1
				break
	# print(red_c , white_c)
	return [red_c , white_c]


def genConstraint( guess , feedback):

	









if __name__ == "__main__":

	secret = [ random.randint(1, NUM_COLS) for peg in range(NUM_PEGS) ]
	print(secret)
	solver = Solver()
	cells_c = basicConstraints()
	solver.add(cells_c)
	if solver.check() == sat:
		m = solver.model()
		r = [[m.evaluate(matrix[i][j]) for j in range(NUM_COLS)] for i in range (NUM_PEGS)]
		guess = calcGuess(r)
		feedback = redWhiteCount(r,secret,guess)
		genConstraint( guess , feedback )
	else: 
		print("lost")
	# redWhiteCount
	# print(solver.check())
	# print(solver.model())

	# addConstraint()