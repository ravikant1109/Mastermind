from z3 import *
import random
from functools import reduce
from itertools import *
import copy


NUM_COLS = 15
NUM_PEGS = 5
NUM_TURNS = 16


# matrix of size ( pegs * colors )
matrix = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(NUM_COLS) ]
	  for i in range(NUM_PEGS) ]
# print(matrix)


def basicConstraints():

	# Each cell of the matrix has value 0 or 1. 1 represents that ith peg(row) has jth color(coloumn)
	cells_c = [ And(0 <= matrix[i][j] , matrix[i][j] <=1) for j in range(NUM_COLS) 
	  for i in range(NUM_PEGS) ]
	# Each row must have exactly 1 cell's value as 1 
	row_c = [And( sum(i) == 1) for i in matrix]
	return cells_c + row_c



def calcGuess(m):

	#guess will have the predicted sequence of colors by player 2 in each turn
	guess = []
	for i in range(NUM_PEGS):
		for j in range(NUM_COLS):
			if m[i][j] == 1:
				guess.append(j+1)
	return guess

#Count the number of red and white feedback
def redWhiteCount(m , secret_c , guess_c):


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

	if 1 == random.randint(1, 30):
		# print("Random hit")
		red_c = random.randint(1, NUM_PEGS)
		white_c = random.randint(1 , NUM_PEGS)

	return [red_c , white_c]

#Generate constraint using red feedback and red+white feedback.
def genConstraint( guess , feedback):

	cons = []
	r = [[matrix[i][j-1] for i in range(NUM_PEGS)] for j in guess]
	if feedback == [0,0]:
		cons = [And(sum(i) == 0) for i in r]
	else:
		x = []
		for i in range(NUM_PEGS):
			x.append(matrix[i][guess[i]-1])

		cons.append(sum(x) == feedback[0])
		y = []
		for i in guess:
			for j in range(NUM_PEGS):
				y.append(matrix[j][i-1])

		cons.append(sum(y) >= sum(feedback))

	return cons

#Display each turn's guess with feedback count
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



# 1 round of Mastermind game
def play():

	secret = [ random.randint(1, NUM_COLS) for peg in range(NUM_PEGS) ]
	# secret = [ 2 , 9 ,10 ,13 ,11]
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
		guess = calcGuess(r)
		feedback = redWhiteCount(r,secret,guess)
		
		# Handle the wrong feedback given by player 1
		newFD = copy.deepcopy(feedback)
		flag = 0
		while(flag !=3 ):
			prevFD = copy.deepcopy(newFD)
			newFD = redWhiteCount(r,secret,guess)
			if prevFD == newFD:
				flag += 1
			else:
				flag = 0
		feedback = newFD

		displayBoard(feedback , guess , turn, secret)
		if feedback[0] == NUM_PEGS:
			print("\nPlayer 2 won in ", turn," turns.")
			break;
		cons = genConstraint( guess , feedback )
		solver.add(cons)
		
	if solver.check() == unsat:
		print("\nunsat: Cannot solve further")


if __name__ == "__main__":

	while(True):

		play()
		if input("Play again? [Y/N]: ") not in ["y","Y"]:
			break