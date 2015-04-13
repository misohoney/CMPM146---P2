import time
import random
from math import *

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None, player = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves() # future child nodes
        self.player = player # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s, p):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s, player = p)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result
"""
Extra code from same source
    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"
    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s
    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s
    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s
"""

def think(rootstate, quip):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    

 #   for i in range(itermax):
      #  node = rootnode
       # state = rootstate.copy()
    if(rootstate.get_whos_turn() == 'blue'):
        player = 'red'
    else:
        player = 'blue'
    rootnode = Node(state = rootstate, player = player)
    beg = time.time()
    end = 0
    roll = 0
    while end < 1: #1 second per turn
        node = rootnode
        state = rootstate.copy()
        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.apply_move(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            lastPlayer = state.get_whos_turn()
            m = random.choice(node.untriedMoves) 
            state.apply_move(m)
            node = node.AddChild(m,state,lastPlayer) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_moves() != []: # while state is non-terminal
            state.apply_move(random.choice(state.get_moves()))
            
        roll += 1
        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            if(node.player == 'red'):
                currScore = state.get_score()['blue']
            else:
                currScore = state.get_score()['red']
            node.Update(state.get_score()[node.player] - currScore) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode
        end = time.time() - beg

    rollText = str(player) + ": Rollouts per second: " + str(roll)
    print(rollText)
    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited