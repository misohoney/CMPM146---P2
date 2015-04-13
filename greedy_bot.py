#Greedy bot chooses a legal move that maximizes the immediate score gain 
#it looks 1 move into the future and chooses the one that increases its score the most
import random

def think(state, quip):
	#gets all the current available legal moves
	legalMoves = state.get_moves() 	
	#setting highestScore to be the current bot's score
	highestScore = 0
	#place a random move if all future moves don't improve score
	greedyMove = random.choice(state.get_moves()) 
	#start looping through all the available legal moves to look 1 move into the future
	for eachMove in legalMoves:
		#copy all the moves into a Temp one
		temp = state.copy()
		#place a move on a Temp one and record its score
		temp.apply_move(eachMove)
		tempScore = temp.get_score()[temp.get_whos_turn()]
		#if Temp move results in a better score, then swap highest score and best move to Temp ones.
		if highestScore < tempScore:
			highestScore = tempScore
			greedyMove = eachMove
	#simply return the move that increase bot's score the most
	return greedyMove

