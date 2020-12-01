from node import *
import maze as mz
import score
import student

import numpy as np
import pandas
import time
import sys
import os

def main():
    maze = mz.Maze("maze_2.csv")
    now_nd = maze.getStartPoint()
    car_dir = Direction.SOUTH
    point = score.Scoreboard("UID_score_maze2.csv")
    interface = student.interface()         #the part of calling student.py was commented out.

    if(sys.argv[1] == '0'):

        while (1):

            #TODO: Impliment your algorithm here and return the UID for evaluation function
            ndList = maze.strategy(now_nd,1,1,0.8)                              #the whole list of nodes should go
            get_UID=interface.wait_for_node()
            while get_UID == '0':
                get_UID=interface.wait_for_node()
            print(type(get_UID))
            print('UID: ',get_UID) #UID from BT
            point.add_UID(get_UID)
            print('1 motion done')

            for next_nd in ndList:                                              #nd: the node should go to //  type : node
                act=int(maze.getAction(car_dir,now_nd,next_nd))
                print('action: ',act)
                interface.send_action(act)   #send action
                car_dir=now_nd.getDirection(next_nd)
                now_nd=next_nd
                get_UID=interface.wait_for_node()
                while get_UID == '0':
                    get_UID=interface.wait_for_node()
                print(type(get_UID))
                print('UID: ',get_UID) #UID from BT
                point.add_UID(get_UID)
                print('1 motion done')
            break

            # ================================================
            # Basically, you will get a list of nodes and corresponding UID strings after the end of algorithm.
			# The function add_UID() would convert the UID string score and add it to the total score.
			# In the sample code, we call this function after getting the returned list. 
            # You may place it to other places, just make sure that all the UID strings you get would be converted.
            # ================================================
            

    elif(sys.argv[1] == '1'):

        while (1):

            #TODO: Implement your algorithm here and return the UID for evaluation function
            input_nd = int(input("destination: "))
            
            if(input_nd == 0):
            	print("end process")
            	print('')
            	break
            end_nd=maze.nd_dict[input_nd]
            ndList = maze.stategy_2(now_nd,end_nd)

            for next_nd in ndList: #nd: the node should go to //  type : node
                interface.send_action(maze.getAction(car_dir,now_nd,next_nd))#send action
                car_dir=now_nd.getDirection(next_nd)
                now_nd=next_nd
                get_UID=interface.wait_for_node()
                while get_UID == '0':
                    get_UID=interface.wait_for_node()
                print(type(get_UID))
                print('UID: ',get_UID) #UID from BT
                point.add_UID(get_UID)
                print('1 motion done')

    """
    node = 0
    while(not node):
        node = interface.wait_for_node()

    interface.end_process()
    """
    print("complete")
    print("")
    a = point.getCurrentScore()
    print("The total score: ", a)

if __name__=='__main__':
    main()
