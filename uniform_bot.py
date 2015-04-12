#Uniform bot chooses amongst legal moves uniformly (use the choice function in Python’s random library
#use the choice function in Python’s random library
import random

def think(state, quip):
	#Return a random element from a list of legal moves
  	return random.choice(state.get_moves()) 

