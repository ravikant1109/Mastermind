from z3 import *
import random
from functools import reduce
from itertools import *
import copy
import sys
import numpy

# numpy.set_printoptions(threshold=sys.maxsize)



# set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)


NUM_COLS = 15
NUM_PEGS = 5
NUM_TURNS = 16

matrix = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(NUM_COLS) ]
	  for i in range(NUM_PEGS) ]

# print(matrix)


def basicConstraints():

	cells_c = [ And(0 <= matrix[i][j] , matrix[i][j] <=1) for j in range(NUM_COLS) 
	  for i in range(NUM_PEGS) ]
	# print(cells_c)
	row_c = [And( sum(i) == 1) for i in matrix]
	return cells_c + row_c



def calcGuess(m):
	guess = []
	for i in range(NUM_PEGS):
		for j in range(NUM_COLS):
			if m[i][j] == 1:
				guess.append(j+1)
	# print("guess===" , guess)
	return guess


def redWhiteCount(m , secret_c , guess_c):

	# print(len(secret) , len(guess))
	secret = copy.deepcopy(secret_c)
	guess = copy.deepcopy(guess_c)
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

	# print("red_c== " , red_c, "white_c==" , white_c)
	return [red_c , white_c]


def genConstraint( guess , feedback):

	cons = []
	r = [[matrix[i][j-1] for i in range(NUM_PEGS)] for j in guess]
	if feedback == [0,0]:
		cons = [And(sum(i) == 0) for i in r]
	else:
		x = []
		for i in range(NUM_PEGS):
			x.append(matrix[i][guess[i]-1])

		
		# print(x)
		cons.append(sum(x) == feedback[0])
		y = []
		for i in guess:
			for j in range(NUM_PEGS):
				y.append(matrix[j][i-1])
		cons.append(sum(y) >= sum(feedback))	


		# cons = [(sum(list( items  for items in sublist for sublist in r))==feedback[0])]
		# cons = sum(cons) ==
		# cons = [And( sum([ matrix[i][j] for i in range(NUM_PEGS)]) == 0) for j in guess]
	# if(len(cons)>1):
	# 	cons = [And(cons)]

	# print(cons)

	return cons


def displayBoard(feedback , guess, turn , secret):

	temp = ""
	if sum(feedback) > 0:
		for i in range(feedback[0]):
			temp += 'r'
		for i in range(feedback[1]):
			temp += 'w'
		print("turn", turn, ":\t", guess ," \t", temp	)
	else:
		print("turn", turn, ":\t", guess)


	# print(guess)
	







def play():

	secret = [ random.randint(1, NUM_COLS) for peg in range(NUM_PEGS) ]
	# secret = [ 8 , 15 ,8 , 10 , 4]
	# print("secret==",secret)
	print("secret key:\t",secret)
	print("-------------------------------------------")
	solver = Solver()
	cells_c = basicConstraints()
	solver.add(cells_c)
	turn = 0

	while solver.check() == sat:
		turn += 1
		m = solver.model()
		r = [[m.evaluate(matrix[i][j]) for j in range(NUM_COLS)] for i in range (NUM_PEGS)]
		# print(r)
		guess = calcGuess(r)
		# print("g---",guess)
		feedback = redWhiteCount(r,secret,guess)
		displayBoard(feedback , guess , turn, secret)
		if feedback[0] == NUM_PEGS:
			print("\nPlayer 2 won in ", turn," turns.")
			break;
		cons = genConstraint( guess , feedback )
		solver.add(cons)
		# solver.check()
		# m = solver.model()
		# r = [[m.evaluate(matrix[i][j]) for j in range(NUM_COLS)] for i in range (NUM_PEGS)]
		# guess = calcGuess(r)
		# feedback = redWhiteCount(r,secret,guess)
		
	if solver.check() == unsat:
		print("\nunsat: Cannot solve further")
	# redWhiteCount
	# print(solver.check())
	# print(solver.model())

	# addConstraint()

if __name__ == "__main__":
	# game = 0

	while(True):
		# game+=1
		# print("Game Number: ", game)
		play()
		if input("Play again? [Y/N]: ") not in ["y","Y"]:
			break