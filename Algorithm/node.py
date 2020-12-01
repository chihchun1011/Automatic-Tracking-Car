import numpy as np
from enum import IntEnum

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST  = 3
    EAST  = 4

def reverse(dir):
    if dir == Direction.NORTH: return Direction.SOUTH
    if dir == Direction.SOUTH: return Direction.NORTH
    if dir == Direction.WEST:  return Direction.EAST
    if dir == Direction.EAST:  return Direction.WEST
    print("invalid Direction")
    return 0

class Node:
    def __init__(self, index=0):
        self.index = index
        self.Successors = []

    def getIndex(self):
        return self.index

    def getSuccessors(self):
        return self.Successors

    def setSuccessor(self, successor, direction, length=1):
        already=False
        for succ in self.Successors:
            if succ[0] == successor :
                already=True
                #TODO: check whether the input of the function is valid by comparing with the class member
        if np.isnan(successor):
            already=True
        #TODO: Update the successors in data members 
        if not already:
            self.Successors.append((successor, direction, length))
        return

    def getSuccessor(self, direction):
        for succ in self.Successors:
            if succ[1]==direction:
                return succ[0] #TODO: Check which successor matches the input corner and return
        # For the valid input, the below part shouldn't be entered
        print("Node(", self.index, ") Successor is not found")
        return 0

    def getDirection(self, nd):
        for succ in self.Successors:
            if succ[0]==nd.getIndex():
                return succ[1] #TODO: Check which successor matches the input direction and return
        # For the valid input, the below part shouldn't be entered
        print("Error in Node.py, getDirection()")
        print("Node(",nd.getIndex(),") is not the Successor of node(",self.index,")")
        return 0

    def isSuccessor(self, nd):
        for succ in self.Successors:
            if succ[0] == nd.getIndex(): return True
        return False

    def isEnd(self):
        return len(self.Successors) == 1 and self.index != 1
