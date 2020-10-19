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

	












if __name__ == "__main__":

	secret = [ random.randint(1, NUM_COLS) for peg in range(NUM_PEGS) ]
	print(secret)
	solver = Solver()
	addConstraint()