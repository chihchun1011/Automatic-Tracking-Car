import pandas
import numpy as np 

# ================================================================
# Scoreboard
#   add_UID(UID_str)
#     UID_str : UID string ("0x" excluded)
#   getCurrentScore()
#     return current score (int)
# ================================================================

class Scoreboard:
    def __init__(self, filepath):
        raw_data = np.array(pandas.read_csv(filepath))#.values

        self.cardList = [int(a, 16) for a in raw_data.T[0]]
        self.visitList = list()
        self.totalScore = 0
        self.cardValue = dict()

        for i in range(len(raw_data)):
            self.cardValue[self.cardList[i]] = raw_data[i][1]

        print ("Successfully read the UID file!")

    def add_UID(self, UID_str):
        UID = int(UID_str,16)

        if UID not in self.cardList:
            print("invalid UID")
        elif UID in self.visitList:
        	print("already visited")
        else:
            point = self.cardValue[UID]
            self.totalScore += point
            print("A treasure is found! You got " + str(point) + " points.")
            print("Current score: "+ str(self.totalScore))
            print("")
            self.visitList.append(UID)

    def getCurrentScore(self):
        return int(self.totalScore)
