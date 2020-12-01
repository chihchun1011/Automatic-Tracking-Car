import node
import numpy as np
import csv
import pandas
import queue
from enum import IntEnum

class Action(IntEnum):
    ADVANCE    = 1
    U_TURN     = 2
    TURN_RIGHT = 3
    TURN_LEFT  = 4
    HALT       = 5

class Maze:
    def __init__(self, filepath):
        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.nd_dict = dict() # key: index, value: the correspond node
        self.explored = set()

        # Update the nodes with the information from raw_data
        for dt in self.raw_data:
            nd=node.Node(dt[0]) #call constructer,dt[0]=csv檔第一欄=index
            self.nodes.append(nd)#ㄍㄨㄛ ㄒㄩㄝˊㄏㄠˇㄋㄢˊㄉㄨㄥˇ
            self.nd_dict[nd.index]=nd
            
        # Update the successors for each node
        for i in range(len(self.nodes)):
            for j in range(1,5):# in csv
                self.nodes[i].setSuccessor(self.raw_data[i][j],j,self.raw_data[i][j+4])
                
    def getStartPoint(self):

        if (len(self.nd_dict) < 2):
            print ("Error: the start point is not included.")
            return 0;
        return self.nd_dict[1]

    def get_treasure_info(self,velocity,turn_time,straight_time):
        ###存寶藏的號碼路徑長期望值時間
        treasure_info = []      #[0=編號，1=路徑長，2=期望值，3=效率值，4=時間]
        treasure_count = -1
        """每個寶藏蒐集資料"""
        for treasure in self.nodes:

            direc_before = 0  ##與前一個點的方向
            direc_after = 0   ##與後一個點的方向

            roadlength = 0    ##寶藏到node"1"的路徑長

            exp_ns = 0     ##南北向位移
            exp_we = 0     ##東西向位移

            straight_node = 0       ##所經過的點中需要繼續直走的點數量
            turn_node = 0     ##所有經過的點中需要轉彎的點數量
           
            if treasure.isEnd() == 1:       ##確定為寶藏
                treasure_info.append([])        ##加入一個陣列
                treasure_count += 1        ##寶藏數+1
                
                treasure_info[treasure_count].append(treasure.getIndex())
                
                path = self.BFS_2(self.nodes[0], treasure)      ##取得1-index路徑

                """for i in range(len(path)):
                    print(path[i].getIndex())"""        ##印出路徑

                
                """BFS_2回傳時刪除起點，此處額外考慮與起點相連處"""
                first_dir = self.nodes[0].getDirection(path [0])
                if len(path)!=1 :
                    second_dir = path [0].getDirection(path [1])
                    if first_dir == second_dir :  straight_node += 1
                if np.isnan(self.raw_data[0][first_dir + 4]):
                    plus=1
                else:
                     plus = self.raw_data[0][first_dir + 4]
                roadlength = plus
                if(first_dir == 1):
                    exp_ns = exp_ns - (plus)     #北取負
                if(first_dir == 2):
                    exp_ns = exp_ns + (plus)     #南取正
                if(first_dir == 3): 
                    exp_we = exp_we - (plus)     #西取負
                if(first_dir == 4): 
                    exp_we = exp_we + (plus)     #東取正
                """-----------------------------------------------------"""
                    
                for i in range(len(path) - 1):
                    direc_after = path [i].getDirection(path [i + 1])     #取得與後一個點的方向
                    
                    if (i != 0):
                        direc_before = path [i-1].getDirection(path [i])    #取得與前一個點的方向
                        if direc_after == direc_before :  straight_node += 1     ##確定同方向前行停頓的個數
                               
                    row = int(path [i].getIndex()-1)        ##列轉為int
                    coloum = direc_after + 4        ##欄不須轉
                    if np.isnan(self.raw_data[row][coloum]):
                        """print("isnan")"""
                        plus=1
                    else:
                        plus = self.raw_data[row][coloum]
                    roadlength = roadlength + plus
                    """print(plus)
                    print(roadlength)
                    print("For i = ",i+1,"roadlength = ",roadlength)"""
                    
                    if(direc_after == 1):
                        exp_ns = exp_ns - (plus)     ##北取負
                    if(direc_after == 2):
                        exp_ns = exp_ns + (plus)     ##南取正
                    if(direc_after == 3): 
                        exp_we = exp_we - (plus)     ##西取負
                    if(direc_after == 4): 
                        exp_we = exp_we + (plus)     ##東取正
                    """print("For i = ",i+1,"exp_ns = ",exp_ns)
                    print("For i = ",i+1,"exp_we = ",exp_we)"""

                turn_node = len(path) - 1 - straight_node
                ##print("From node 1 to node",int(treasure.getIndex()),", through ",straight_node," straight(s)and ",turn_node," turns(s).")    
                treasure_info[treasure_count].append(roadlength)        ##填入路徑長為[1]
                exp = abs(exp_ns) + abs(exp_we)
                treasure_info[treasure_count].append(exp)       ##填入期望值為[2]
                eff = exp/roadlength
                treasure_info[treasure_count].append(round(eff,3))       ##填入效率值為[3]
                time = roadlength/velocity + turn_time*turn_node + straight_time*straight_node
                treasure_info[treasure_count].append(round(time,3))     ##填入時間為[4]
                treasure_info[treasure_count].append(turn_node+straight_node)
                treasure_info[treasure_count].append(turn_node)
                treasure_info[treasure_count].append(straight_node)
        #--------------------這串目前隱藏，妳要用的時候把隱藏拿掉，印出寶藏資訊------------------
        ##print("Treasure's information")
        ##print(treasure_info)        ##印出資料
        #--------------------------------------------------------------------------------------------------
        return(treasure_info,treasure_count)

    def get_connection_info(self,velocity, turn_time, straight_time):

        ###存寶藏的號碼路徑長期望值時間
        treasure_info = self.get_treasure_info(velocity, turn_time, straight_time)[0]
        connection_info = []
        connection_count = -1
        treasure = [] #[0=index,1=Road,2=E,3=E/road]
        treasure_index = []
        direc_before = 0  ##與前一個點的方向
        direc_after = 0   ##與後一個點的方向

        roadlength = 0    ##寶藏到node"1"的路徑長

        exp_ns = 0     ##南北向位移
        exp_we = 0     ##東西向位移

        treasure_count = 0 
        for treasure in self.nodes:
            if treasure.isEnd() == 1:       ##確定為寶藏
                treasure_index.append(treasure.getIndex())        ##加入一個陣列
                treasure_count+=1
        ##print(treasure_count)
        ##print(treasure_index)
        
        length = len(treasure_index)-1
        
        for i in range(length+1):
            g=i
            straight_node = 0       ##所經過的點中需要繼續直走的點數量
            turn_node = 0     ##所有經過的點中需要轉彎的點數量
            connection_info.append([])
            connection_count +=1
            connection_info[connection_count].append(1.0)
            connection_info[connection_count].append(treasure_index[i])
            path = []
            path = self.BFS_2(self.nodes[0],self.nd_dict[treasure_index[i]])
            ########################################################
                
            ##  BFS_2回傳時刪除起點，此處額外考慮與起點相連處
            first_dir = self.nodes[0].getDirection(path [0])
            if len(path)!=1 :
                second_dir = path [0].getDirection(path [1])
                if first_dir == second_dir :  straight_node += 1
            if np.isnan(self.raw_data[0][first_dir + 4]):
                plus=1
            else:
                plus = self.raw_data[0][first_dir + 4]
            roadlength = plus
                
                
            """print("For i =  0","roadlength = ",roadlength)
                print("For i =  0","exp_ns = ",exp_ns)
                print("For i =  0","exp_we = ",exp_we)"""

            ########################################################
            for i in range(len(path) - 1):
                    direc_after = path [i].getDirection(path [i + 1])     #取得與後一個點的方向
                    
                    if (i != 0):
                        direc_before = path [i-1].getDirection(path [i])    #取得與前一個點的方向
                        if direc_after == direc_before :
                            straight_node += 1     ##確定同方向前行停頓的個數
                            ##print(path [i-1].getIndex()," to ",path [i].getIndex(),"is straight")
                    
                    row = int(path [i].getIndex()-1)        ##列轉為int
                    coloum = direc_after + 4        ##欄不須轉
                    if np.isnan(self.raw_data[row][coloum]):
                        """print("isnan")"""
                        plus=1
                    else:
                        plus = self.raw_data[row][coloum]
                    roadlength = roadlength + plus
                    """print(plus)
                    print(roadlength)
                    print("For i = ",i+1,"roadlength = ",roadlength)"""
                   
            turn_node = len(path) - 1 - straight_node
            ##print("From node 1 to node",int(treasure_index[i]),", through ",straight_node," straight(s)and ",turn_node," turns(s).")    
            connection_info[connection_count].append(roadlength)        ##填入路徑長為[2]
            time = roadlength/velocity + turn_time*turn_node + straight_time*straight_node
            connection_info[connection_count].append(round(time,3))
            expectation = treasure_info[ g ][ 2 ]
            ##print(treasure_info[ g ][ 0 ],end=" ")
            ##print(expectation)
            point_per_time =  expectation/time
            connection_info[connection_count].append(round(point_per_time,3))
        ##print(connection_info)
        """ for i in range(length+1):
            for j in range(len(treasure_index)-1-i):"""
        for i in range(length+1):
            for j in range(length+1):
                if i==j :   continue
                ##print("here",i,j)
                straight_node = 0       ##所經過的點中需要繼續直走的點數量
                turn_node = 0     ##所有經過的點中需要轉彎的點數量
                connection_info.append([])
                connection_count +=1
                ##print("from ",treasure_index[i]," to ",treasure_index[i+j+1])
                connection_info[connection_count].append(treasure_index[i])
                connection_info[connection_count].append(treasure_index[j])
                 
                path = []
               ###i+j+1
                path = self.BFS_2(self.nd_dict[treasure_index[i]],self.nd_dict[treasure_index[j]])
                ########################################################
                
                ##  BFS_2回傳時刪除起點，此處額外考慮與起點相連處
                first_dir = self.nd_dict[treasure_index[i]].getDirection(path[0])
                if len(path)!=1 :
                    second_dir = path [0].getDirection(path [1])
                    if first_dir == second_dir :  straight_node += 1
                    if np.isnan(self.raw_data[0][first_dir + 4]):
                        plus=1
                    else:
                        plus = self.raw_data[0][first_dir + 4]
                roadlength = plus
                
                ########################################################
                for t in range(len(path) - 1):
                        direc_after = path [t].getDirection(path [t + 1])     #取得與後一個點的方向
                    
                        if (t != 0):
                            direc_before = path [t-1].getDirection(path [t])    #取得與前一個點的方向
                            if direc_after == direc_before :
                                straight_node += 1     ##確定同方向前行停頓的個數
                                ##print(path [i-1].getIndex()," to ",path [i].getIndex(),"is straight")
                    
                        row = int(path [t].getIndex()-1)        ##列轉為int
                        coloum = direc_after + 4        ##欄不須轉
                        if np.isnan(self.raw_data[row][coloum]):
                            """print("isnan")"""
                            plus=1
                        else:
                            plus = self.raw_data[row][coloum]
                        roadlength = roadlength + plus
                        """print(plus)
                        print(roadlength)
                        print("For i = ",i+1,"roadlength = ",roadlength)"""
                   
                turn_node = len(path) - 1 - straight_node
                ##print("From node 1 to node",int(treasure_index[i]),", through ",straight_node," straight(s)and ",turn_node," turns(s).")
                ##print("roadlength : ",roadlength)
                
                connection_info[connection_count].append(roadlength)        ##填入路徑長為[2]
                time = roadlength/velocity + turn_time*turn_node + straight_time*straight_node
                connection_info[connection_count].append(round(time,3))
                expectation = treasure_info[ j ][ 2 ]
                point_per_time =  expectation/time
                connection_info[connection_count].append(round(point_per_time,3))
        """print("Treasure_info：")           
        print(treasure_info)
        print("Connection_info：")
        print(connection_info)
        print("treasure_count",treasure_count)"""
        return(connection_info,treasure_count)
    
        """BFS是最少node可以跳過"""
    def BFS(self, nd):
        # Design your data structure here for your algorithm
        ##print("After go into BFS, nd = ",nd)
        ndList = [] 
        self.explored.add(nd.index)
        ##print("INNNNNNNN self.explored : ",self.explored)
        n=queue.Queue()
        n.put(nd)
        visited=set()
        visited.add(nd.index)#ㄨㄣˊㄧㄢˊㄉㄜ˙ㄍㄨㄛ ㄒㄩㄝˊ
        transitiontable=dict()
        endnode=nd #type:node
        
        # Apply your algorithm here. Make sure your algorithm can update values and stop under some conditions.
        while (True):
            sucnum=0
            if n.empty():
                ##print("Visited",visited)
                break
            checking_nd=n.get()#get a nd
            #print("Check",checking_nd)
            for succ in checking_nd.Successors:
                sucnum+=1 #count the successors of nd
                if succ[0] not in visited :
                    visited.add(succ[0])
                    
                    transitiontable[succ[0]]=checking_nd
                    n.put(self.nodes[int(succ[0])-1])
            #print("sucnum",sucnum)
            if sucnum==1:
                endnode=checking_nd
                if endnode.index not in self.explored:
                    ##print("Visited",visited)
                    break
        #Update the information of your data structure
        node=endnode #type:node
        ##print("self.explored : ",self.explored)
        if node.index in self.explored:
            ##print("node.index in self.explored",ndList)
            return ndList
        ndList.append(node)
        while node.index != nd.index:
            prenode =transitiontable[node.index]
            ndList.append(prenode)
            self.explored.add(node.index)
            node = prenode
        ndList.reverse()
        del ndList[0]
        ##print("return",ndList)
        return ndList #type:list of type node

    def BFS_origin_add_all(self,nd):
        ##print("After go into BFS_origin_add_all, nd = ",nd)
        ##print(self.explored)
        self.explored=set()
        path=[]
        part_path=self.BFS(nd)
       ## print("BFS_origin_add_all = ",part_path)
        while len(part_path)>0:
            path+=part_path
            nd=part_path[-1]
            part_path=self.BFS(nd)
       
        #for j in range(len(path)):  
            #print(int(path[j].getIndex()),end=", ")
        return path
       
    
    def BFS_efficiency(self, nd, velocity, turn_time, straight_time):
        copy_treasure = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        ori_t  = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        treasure_count = self.get_treasure_info(velocity,turn_time,straight_time)[1]
        
        """泡沫排序法"""
        for i in range(treasure_count ):       
            for j in range(treasure_count  - i):
                if copy_treasure[j][3] < copy_treasure[j+1][3]:     ##效率值大交換
                    copy_treasure[j],copy_treasure[j+1]=copy_treasure[j+1],copy_treasure[j]
                    
        """存取編號與轉資料型態"""
        treasure_sequence = []      ##依效率值排序，資料型態int(存編號)
        treasure_return = []        ##依效率值排序，資料型態Node
        for i in range(treasure_count + 1 ):       
            treasure_sequence.append(int(copy_treasure [i][0]))      ##存編號
            treasure_return.append(self.nd_dict[treasure_sequence[i]])      ##轉int成Node
        ##print("treasure_return",treasure_return)

        """寶藏順序擴展成節點順序"""
        path_sequence = []      ##存要走的路徑，資料型態Node
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))      ##Node1到第一個寶藏
        
        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            ##print(self.BFS_2(treasure_return[t],treasure_return[t+1]))
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))     ##寶藏到寶藏

        """Print 區"""
        """print("Treasures' efficiencies：")
        print("[",end="")
        for f in range(len(ori_t)):
            if f == len(ori_t)-1 :
                print(int(ori_t[f][0]),end=" : ")
                print('%.3f' %(ori_t[f][3]),end="")
                break
            print(int(ori_t[f][0]),end=" : ")
            print('%.3f' % ori_t[f][3],end=", ")  
        print("]")
        print("")
        print("Treasures arranged by their efficiencies : ")
        print((treasure_sequence))
        print("")
        print("Path sequence：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range(len(copy_treasure)):
                            
                if int(path_sequence[j].getIndex())== copy_treasure[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")"""

        """回傳順序"""
        return path_sequence
#------------------------------------ 我是分隔線   -----------------------------------------------     
    def BFS_expectation(self, nd, velocity, turn_time, straight_time):
        copy_treasure = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        ori_t  = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        treasure_count = self.get_treasure_info(velocity,turn_time,straight_time)[1]
        
        for i in range(treasure_count ):       ##泡沫排序法
            for j in range(treasure_count  - i):
                if copy_treasure[j][2] < copy_treasure[j+1][2]:     ##期望值大交換
                    copy_treasure[j],copy_treasure[j+1]=copy_treasure[j+1],copy_treasure[j]
                    
        treasure_sequence = []      ##依期望值排序
        treasure_return = []
        
        for i in range(treasure_count + 1 ):       
            treasure_sequence.append(int(copy_treasure [i][0]))
            treasure_return.append(self.nd_dict[treasure_sequence[i]])
       
        path_sequence = []
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))

        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))
        
        """print("Treasures' expectations：")
        print("[",end="")
        for f in range(len(ori_t)):
            if f == len(ori_t)-1 :
                print(int(ori_t[f][0]),end=" : ")
                print(int(ori_t[f][2]),end="")
                break
            print(int(ori_t[f][0]),end=" : ")
            print(int(ori_t[f][2]),end=", ")
        print("]")
        print("")
        print("Treasures arranged by their expectations : ")
        print((treasure_sequence))
        print("")
        print("Path sequence：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range(len(copy_treasure)):
                            
                if int(path_sequence[j].getIndex())== copy_treasure[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")"""
        return path_sequence

    def BFS_roadlength(self, nd, velocity, turn_time, straight_time):
        copy_treasure = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        ori_t  = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        treasure_count = self.get_treasure_info(velocity,turn_time,straight_time)[1]
        for i in range(treasure_count ):       ##泡沫排序法
            for j in range(treasure_count  - i):
                if copy_treasure[j][1] < copy_treasure[j+1][1]:     ##路徑長大交換
                    copy_treasure[j],copy_treasure[j+1]=copy_treasure[j+1],copy_treasure[j]
        treasure_sequence = []      ##依路徑長排序
        treasure_return = []
        for i in range(treasure_count ):       
            treasure_sequence.append(copy_treasure [i][0])
            treasure_return.append(self.nd_dict[nd.index])

        treasure_sequence = []      ##依期望值排序
        treasure_return = []
        
        for i in range(treasure_count + 1 ):       
            treasure_sequence.append(int(copy_treasure [i][0]))
            treasure_return.append(self.nd_dict[treasure_sequence[i]])
        ##print("treasure_return",treasure_return)
       
        path_sequence = []
        ##print("len of treasure_return",len(treasure_return))
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))
        ##print(path_sequence)
        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            
            ##print(self.BFS_2(treasure_return[t],treasure_return[t+1]))
            
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))
        ##print("path_sequence",path_sequence)
        
        
        """print("Treasures' roadlengths：")
        print("[",end="")
        for f in range(len(ori_t)):
            if f == len(ori_t)-1 :
                print(int(ori_t[f][0]),end=" : ")
                print(int(ori_t[f][1]),end="")
                break
            print(int(ori_t[f][0]),end=" : ")
            print(int(ori_t[f][1]),end=", ")
        print("]")
        print("")
        print("Treasures arranged by their roadlengths : ")
        print((treasure_sequence))
        print("")
        print("Path sequence：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range(len(copy_treasure)):
                            
                if int(path_sequence[j].getIndex())== copy_treasure[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")"""
        
        return path_sequence
        
    def BFS_time(self, nd, velocity, turn_time, straight_time):
        copy_treasure = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        ori_t  = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        treasure_count = self.get_treasure_info(velocity,turn_time,straight_time)[1]
        for i in range(treasure_count ):       ##泡沫排序法
            for j in range(treasure_count  - i):
                if copy_treasure[j][4] > copy_treasure[j+1][4]:     ##時間短交換
                    copy_treasure[j],copy_treasure[j+1]=copy_treasure[j+1],copy_treasure[j]
        treasure_sequence = []      ##依時間短排序
        treasure_return = []
        for i in range(treasure_count ):       
            treasure_sequence.append(copy_treasure [i][0])
            treasure_return.append(self.nd_dict[nd.index])
        treasure_sequence = []      ##依期望值排序
        treasure_return = []
        
        for i in range(treasure_count + 1 ):       
            treasure_sequence.append(copy_treasure [i][0])
            treasure_return.append(self.nd_dict[treasure_sequence[i]])
        ##print("treasure_return",treasure_return)
       
        path_sequence = []
        ##print("len of treasure_return",len(treasure_return))
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))
        ##print(path_sequence)
        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            
            ##print(self.BFS_2(treasure_return[t],treasure_return[t+1]))
            
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))
        ##print("path_sequence",path_sequence)
        """print("Treasures' indices : ")
        print("[",end="")
        for f in range(len(ori_t)):
            if f == len(ori_t)-1 :
                print(int(ori_t[f][0]),end="]")
                break
            print(int(ori_t[f][0]),end=", ")
        print("")
        print("")
        print("Treasure path's informations : ")
        for g in range(len(ori_t)):
            print("[Treasure : ",int(ori_t[g][0]),"Node : ",int(ori_t[g][5]),"Turn : ",int(ori_t[g][6]),"Straight : ",int(ori_t[g][7]),"]")
        print("")
        print("Car's parameters : ")
        print("Velocity : ",velocity)
        print("Turning time : ",turn_time)
        print("Stop and go ahead time : ",straight_time)
        print("")
        print("Calaulations : ")
        for h in range(len(ori_t)):
            print("[Treasure : ",int(ori_t[h][0]),"]  [",int(ori_t[h][1]),"] ÷ [",velocity,"] + [",turn_time,"] × [",int(ori_t[h][6]),"] + [",straight_time,"] × [",int(ori_t[h][7]),"] = [",ori_t[h][4],"]")
        print("")
        print("Treasures arranged by their travel times : ")
        print((treasure_sequence))
        print("")
        print("Path sequence：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range(len(copy_treasure)):
                            
                if int(path_sequence[j].getIndex())== copy_treasure[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")   
        ##print("]")"""
        
        
        return path_sequence
      
    def BFS_time_enhancement(self, nd, velocity, turn_time, straight_time):
        connection_info = self.get_connection_info(velocity,turn_time,straight_time)[0]     ##存兩寶藏連線資料
        treasure_info = self.get_treasure_info(velocity,turn_time,straight_time)[0]     ##存寶藏資料
        treasure_number = self.get_connection_info(velocity,turn_time,straight_time)[1]     ##存寶藏個數
        """print("Treasure_info：")           
        print(treasure_info)
        print("Connection_info：")
        print(connection_info)
        print("treasure_number",treasure_number)"""
        
        """排序"""
        travel_point = []       ##經過的點
        for i in range(treasure_number -1 ):       ##泡沫排序法(只排起點為1)
            for j in range(treasure_number -1  - i):
                if connection_info[j][3] > connection_info[j+1][3]:     ##時間長於後者，交換
                    connection_info[j],connection_info[j+1]=connection_info[j+1],connection_info[j]
        travel_point.append(int(connection_info[0][1]))
        ##print(travel_point)
        for t_num in range(treasure_number  ):      ##總共有treasure_number個起點要排序
            for i in range(treasure_number -2 ):       ##泡沫排序法(任意寶藏為起點，但只有相同起點的要排序)
                for j in range(treasure_number -2  - i):
                    k = treasure_number + (treasure_number-1)*t_num + j
                    if connection_info[k][3] > connection_info[k+1][3]:     ##時間長於後者，交換
                        connection_info[k],connection_info[k+1]=connection_info[k+1],connection_info[k]
        """print("ARR　Connection_info：")
        print(connection_info) """

        """挑選路徑"""
        for t_num in range(treasure_number-1):  
            last_treasure = travel_point [len(travel_point)-1]      ##已選好路徑的最後寶藏
            ##print("last_treasure",last_treasure)
            
            for Q in range(len(connection_info)):
                true = 1      ##true=1，新的寶藏；true=0，已找過
                if connection_info[Q][0] !=last_treasure:
                    ##print("起點錯誤",connection_info[Q][0],end=" ")
                    continue      ##起點錯誤，找下一個
                """起點正確才會到這裡"""
                for visited in travel_point:
                    if connection_info[Q][1] == visited :       ##已找過
                        ##print("重覆編號",connection_info[Q][1])
                        true = 0
                if true ==0:
                    continue      ##已找過，找下一個
                if true ==1:
                    ##print("正確編號",connection_info[Q][1])
                    travel_point.append(int(connection_info[Q][1]))
                    break
                
            ##print(travel_point)

        """存取編號與轉資料型態"""
        treasure_return = []        ##依效率值排序，資料型態Node
        for o in range(len(travel_point)):       
            treasure_return.append(self.nd_dict[travel_point[o]])      ##轉int成Node
        ##print("treasure_return",treasure_return)
            
        """寶藏順序擴展成節點順序"""
        path_sequence = []      ##存要走的路徑，資料型態Node
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))      ##Node1到第一個寶藏
        
        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            ##print(self.BFS_2(treasure_return[t],treasure_return[t+1]))
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))     ##寶藏到寶藏

        """Print 區"""
        """print("Treasures' indices : ")
        print("[2, 3, 6, 17, 19, 21, 25, 34, 35, 38]")
        print("")
        print("Car's parameters : ")
        print("Velocity : ",velocity)
        print("Turning time : ",turn_time)
        print("Stop and go ahead time : ",straight_time)
        print("")
        ##print("path_sequence",path_sequence)
        print("Treasures arranged by their travel times (enhance version) : ")
        print(travel_point)
        print("")
        print("Path_sequence ：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range((treasure_number)):
                            
                if int(path_sequence[j].getIndex())== treasure_info[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")"""
        """for j in range(len(path_sequence)):
            print(path_sequence[j].getIndex(),end=" ")
        print("]")"""

        """回傳順序"""
        return path_sequence

    def BFS_roadlength_enhancement(self, nd, velocity, turn_time, straight_time):
        connection_info = self.get_connection_info(velocity,turn_time,straight_time)[0]     ##存兩寶藏連線資料
        treasure_info = self.get_treasure_info(velocity,turn_time,straight_time)[0]     ##存寶藏資料
        treasure_number = self.get_connection_info(velocity,turn_time,straight_time)[1]     ##存寶藏個數
        """print("Treasure_info：")           
        print(treasure_info)
        print("Connection_info：")
        print(connection_info)
        print("treasure_number",treasure_number)"""
        
        """排序"""
        travel_point = []       ##經過的點
        for i in range(treasure_number -1 ):       ##泡沫排序法(只排起點為1)
            for j in range(treasure_number -1  - i):
                if connection_info[j][2] > connection_info[j+1][2]:     ##時間長於後者，交換
                    connection_info[j],connection_info[j+1]=connection_info[j+1],connection_info[j]
        travel_point.append(int(connection_info[0][1]))
        ##print(travel_point)
        for t_num in range(treasure_number  ):      ##總共有treasure_number個起點要排序
            for i in range(treasure_number -2 ):       ##泡沫排序法(任意寶藏為起點，但只有相同起點的要排序)
                for j in range(treasure_number -2  - i):
                    k = treasure_number + (treasure_number-1)*t_num + j
                    if connection_info[k][2] > connection_info[k+1][2]:     ##時間長於後者，交換
                        connection_info[k],connection_info[k+1]=connection_info[k+1],connection_info[k]
        """print("ARR　Connection_info：")
        print(connection_info) """

        """挑選路徑"""
        for t_num in range(treasure_number-1):  
            last_treasure = travel_point [len(travel_point)-1]      ##已選好路徑的最後寶藏
            ##print("last_treasure",last_treasure)
            
            for Q in range(len(connection_info)):
                true = 1      ##true=1，新的寶藏；true=0，已找過
                if connection_info[Q][0] !=last_treasure:
                    ##print("起點錯誤",connection_info[Q][0],end=" ")
                    continue      ##起點錯誤，找下一個
                """起點正確才會到這裡"""
                for visited in travel_point:
                    if connection_info[Q][1] == visited :       ##已找過
                        ##print("重覆編號",connection_info[Q][1])
                        true = 0
                if true ==0:
                    continue      ##已找過，找下一個
                if true ==1:
                    ##print("正確編號",connection_info[Q][1])
                    travel_point.append(int(connection_info[Q][1]))
                    break
                
            ##print(travel_point)

        """存取編號與轉資料型態"""
        treasure_return = []        ##依效率值排序，資料型態Node
        for o in range(len(travel_point)):       
            treasure_return.append(self.nd_dict[travel_point[o]])      ##轉int成Node
        ##print("treasure_return",treasure_return)
            
        """寶藏順序擴展成節點順序"""
        path_sequence = []      ##存要走的路徑，資料型態Node
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))      ##Node1到第一個寶藏
        
        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            ##print(self.BFS_2(treasure_return[t],treasure_return[t+1]))
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))     ##寶藏到寶藏

        """Print 區"""
        """print("Treasures' indices : ")
        print("[2, 3, 6, 17, 19, 21, 25, 34, 35, 38]")
        print("")
        ##print("path_sequence",path_sequence)
        print("Treasures arranged by their roadlengths (enhance version) : ")
        print(travel_point)
        print("")
        print("Path_sequence ：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range((treasure_number)):
                            
                if int(path_sequence[j].getIndex())== treasure_info[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")
        ##for j in range(len(path_sequence)):
        ##    print(path_sequence[j].getIndex(),end=" ")
        ##print("]")"""

        return path_sequence
    
    def BFS_efficiency_enhancement(self, nd, velocity, turn_time, straight_time):
        connection_info = self.get_connection_info(velocity,turn_time,straight_time)[0]     ##存兩寶藏連線資料
        treasure_info = self.get_treasure_info(velocity,turn_time,straight_time)[0]     ##存寶藏資料
        treasure_number = self.get_connection_info(velocity,turn_time,straight_time)[1]     ##存寶藏個數
        """print("Treasure_info：")           
        print(treasure_info)
        print("Connection_info：")
        print(connection_info)
        print("treasure_number",treasure_number)"""
        
        """排序"""
        travel_point = []       ##經過的點
        for i in range(treasure_number -1 ):       ##泡沫排序法(只排起點為1)
            for j in range(treasure_number -1  - i):
                if connection_info[j][4] < connection_info[j+1][4]:     ##時間長於後者，交換
                    connection_info[j],connection_info[j+1]=connection_info[j+1],connection_info[j]
        travel_point.append(int(connection_info[0][1]))
        ##print(travel_point)
        for t_num in range(treasure_number  ):      ##總共有treasure_number個起點要排序
            for i in range(treasure_number -2 ):       ##泡沫排序法(任意寶藏為起點，但只有相同起點的要排序)
                for j in range(treasure_number -2  - i):
                    k = treasure_number + (treasure_number-1)*t_num + j
                    if connection_info[k][4] < connection_info[k+1][4]:     ##時間長於後者，交換
                        connection_info[k],connection_info[k+1]=connection_info[k+1],connection_info[k]
        ##print("ARR　Connection_info：")
        ##print(connection_info) 

        """挑選路徑"""
        for t_num in range(treasure_number-1):  
            last_treasure = travel_point [len(travel_point)-1]      ##已選好路徑的最後寶藏
            ##print("last_treasure",last_treasure)
            
            for Q in range(len(connection_info)):
                true = 1      ##true=1，新的寶藏；true=0，已找過
                if connection_info[Q][0] !=last_treasure:
                    ##print("起點錯誤",connection_info[Q][0],end=" ")
                    continue      ##起點錯誤，找下一個
                """起點正確才會到這裡"""
                for visited in travel_point:
                    if connection_info[Q][1] == visited :       ##已找過
                        ##print("重覆編號",connection_info[Q][1])
                        true = 0
                if true ==0:
                    continue      ##已找過，找下一個
                if true ==1:
                    ##print("正確編號",connection_info[Q][1])
                    travel_point.append(int(connection_info[Q][1]))
                    break
                
            ##print(travel_point)

        """存取編號與轉資料型態"""
        treasure_return = []        ##依效率值排序，資料型態Node
        for o in range(len(travel_point)):       
            treasure_return.append(self.nd_dict[travel_point[o]])      ##轉int成Node
        ##print("treasure_return",treasure_return)
            
        """寶藏順序擴展成節點順序"""
        path_sequence = []      ##存要走的路徑，資料型態Node
        path_sequence.extend(self.BFS_2(self.nodes[0],treasure_return[0]))      ##Node1到第一個寶藏
        
        """for i in range(len(treasure_return)):
            print("treasure_return[",i,"]",treasure_return[i].getIndex())"""
        for t in range(len(treasure_return)-1):
            ##print(self.BFS_2(treasure_return[t],treasure_return[t+1]))
            path_sequence.extend((self.BFS_2(treasure_return[t],treasure_return[t+1])))     ##寶藏到寶藏

        """Print 區"""
        """print("Treasures' indices : ")
        print("[2, 3, 6, 17, 19, 21, 25, 34, 35, 38]")
        print("")
        print("Car's parameters : ")
        print("Velocity : ",velocity)
        print("Turning time : ",turn_time)
        print("Stop and go ahead time : ",straight_time)
        print("")
        ##print("path_sequence",path_sequence)
        print("Treasures arranged by their efficiencies (enhance version) : ")
        print(travel_point)
        print("")
        print("Path_sequence ：")
        print("[",end="")
        for j in range(len(path_sequence)):
            for w in range((treasure_number)):
                            
                if int(path_sequence[j].getIndex())== treasure_info[w][0]:
                    treasure_det = 1
                    print(int(path_sequence[j].getIndex()),end="]")
                    print("")
                    if j != len(path_sequence)-1 :
                        print("[",end="")
                    continue
            if j == len(path_sequence)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(path_sequence[j].getIndex()),end=", ")
        ##for j in range(len(path_sequence)):
        ##    print(path_sequence[j].getIndex(),end=" ")
        ##print("]")"""

        """回傳順序"""
        return path_sequence
    
    def BFS_2(self, nd_from, nd_to):
        """ return a sequence of nodes of the shortest path"""
        #TODO: similar to BFS but fixed start point and end point
        ndList = []
        n=queue.Queue()
        n.put(nd_from)
        visited=set()
        visited.add(nd_from.index)
        transitiontable=dict()

        while True:
            if n.empty():
                break
            checking_nd=n.get() #type:node
            for succ in checking_nd.Successors:
                if succ[0] not in visited :
                    visited.add(succ[0])
                    transitiontable[succ[0]]=checking_nd
                    if succ[0]==nd_to.index:
                        break
                    n.put(self.nodes[int(succ[0])-1])

        node=nd_to #type:node
        
        ndList.append(node)
        ##print(len(ndList))
        ##for g in range(len(ndList)
        ##print(ndList[1])
        while node.index != nd_from.index:
            prenode =transitiontable[node.index]
            ##print("prenode",prenode.getIndex())
            ndList.append(prenode)
            self.explored.add(node.index)
            node = prenode
            ##print(node.getIndex())
        ndList.reverse()
        ##print(len(ndList))
        del ndList[0]
        
        return ndList

    def getAction(self, car_dir, nd_from, nd_to):
        """ return an action and the next direction of the car """
        if nd_from.isSuccessor(nd_to):
            nd_dir = nd_from.getDirection(nd_to)
            # Return the action based on the current car direction and the direction to next node
            if car_dir == 1:
                if nd_dir == 1: return 1
                if nd_dir == 2: return 2
                if nd_dir == 3: return 4
                if nd_dir == 4: return 3
            if car_dir == 2:
                if nd_dir == 1: return 2
                if nd_dir == 2: return 1
                if nd_dir == 3: return 3
                if nd_dir == 4: return 4
            if car_dir == 3:
                if nd_dir == 1: return 3
                if nd_dir == 2: return 4
                if nd_dir == 3: return 1
                if nd_dir == 4: return 2
            if car_dir == 4:
                if nd_dir == 1: return 4
                if nd_dir == 2: return 3
                if nd_dir == 3: return 2
                if nd_dir == 4: return 1
            print("Error: Failed to get the action")
            return 0
        else:
            print("Error: Node(",nd_to.getIndex(),") is not the Successor of Node(",nd_from.getIndex(),")")
            return 0
        
    def score_estimate(self,path,velocity, turn_time, straight_time):
        print("_________________________Score_estimate_________________________________")
        treasure_info = self.get_treasure_info(velocity,turn_time,straight_time)[0]
        #print(treasure_info)
        u_turn_time = 2
        path_index = []
        time = 0
        for i in range(len(path)):
            path_index.append(path[i].getIndex())
        print(path_index)
        score = 0

        direc_before = 0  ##與前一個點的方向
        direc_after = 0   ##與後一個點的方向

        roadlength = 0    ##寶藏到node"1"的路徑長

        """BFS_2回傳時刪除起點，此處額外考慮與起點相連處"""
        ##print(self.nodes[0].getIndex())
        ##print("gjk",path [0].getIndex())
        first_dir = self.nodes[0].getDirection(path [0])
        
        if len(path)!=1 :
            second_dir = path [0].getDirection(path [1])
            if first_dir == second_dir :  action_type = 1
            else : action_type = 2
        if np.isnan(self.raw_data[0][first_dir + 4]):
            plus=1
        else : 
            plus = self.raw_data[0][first_dir + 4]
        roadlength = plus        
        time += roadlength/velocity
        if action_type == 1:
            time += straight_time
        if action_type == 2:
            time += turn_time
        #print("Roadlength is :",roadlength,"Time is : ",time)
        """-----------------------------------------------------"""
        
        for i in range(len(path) - 1):
            
            action_type = 0
            #print("歸零",action_type)
            direc_after = path [i].getDirection(path [i + 1])     #取得與後一個點的方向        
            if (i != 0):
                direc_before = path [i-1].getDirection(path [i])    #取得與前一個點的方向
                if direc_after - direc_before ==0 :
                    action_type = 1     #直走
                    time += straight_time
                if (direc_after != direc_before) and path[i].isEnd() == 0 :
                    action_type = 2     #轉彎
                    time += turn_time
                if path[i].isEnd() == 1:
                    action_type  =3    #迴轉
                    time += u_turn_time

            if path[i].isEnd() == 1:    #迴轉
                for s in range(len(treasure_info)):
                    if treasure_info[s][0] == path[i].getIndex():
                        
                        score += treasure_info[s][2]
                        #print("At",path[i].getIndex(),"Score : ",score,"exp",treasure_info[s][2])
                               
            row = int(path [i].getIndex()-1)        ##列轉為int
            coloum = direc_after + 4        ##欄不須轉
            if np.isnan(self.raw_data[row][coloum]):
                """print("isnan")"""
                plus=1
            else:
                plus = self.raw_data[row][coloum]
            time += plus/velocity
            roadlength = roadlength + plus
            
            """if i !=len(path):
                print("At",path[i].getIndex(),"Roadlength is :",roadlength-plus,"Plus",plus,"Time is : ",round(time,1),end=" ")    
                if action_type == 0:
                    print("錯誤")
                    "break"
                if action_type == 1:
                    print("After",direc_after,"Before",direc_before,end=" ")
                    print("直走")
                if action_type == 2:
                    print("After",direc_after,"Before",direc_before,end=" ")
                    print("轉彎")
                if action_type == 3:
                    print("After",direc_after,"Before",direc_before,end=" ")
                    print("迴轉")"""

            if time>200:
                break
        if i==(len(path)-2):
            for s in range(len(treasure_info)):
                if treasure_info[s][0] == path[i+1].getIndex():    
                    score += treasure_info[s][2]
            
        print("Total Roadlength is :",roadlength,"Time is : ",round(time,1),"Score is : ",score)
        return score
        
            
        
    def strategy(self, nd,velocity, turn_time, straight_time):
        tre = self.get_treasure_info(velocity, turn_time, straight_time)[0]
        ##print("Before go into BFS_origin_add_all, nd = ",nd)
        pathA = self.BFS_origin_add_all(nd)
        ##print("patha",pathA)
        pointA = self.score_estimate(pathA,velocity, turn_time, straight_time)
        print("Node : ",pointA)
        Max = pathA
        best = pointA
        pathB = self.BFS_roadlength(nd,velocity,turn_time, straight_time)
        pointB = self.score_estimate(pathB,velocity, turn_time, straight_time)
        print("Roadlength : ",pointB)
        if(pointB>=best):
            Max = pathB
            best = pointB
        pathC = self.BFS_expectation(nd,velocity,turn_time, straight_time)
        pointC = self.score_estimate(pathC,velocity, turn_time, straight_time)
        print("Expectation : ",pointC)
        if(pointC>=best):
            Max = pathC
            best = pointC
        pathD = self.BFS_efficiency(nd,velocity,turn_time, straight_time)
        pointD = self.score_estimate(pathD,velocity, turn_time, straight_time)
        print("Efficiency : ",pointD)
        if(pointD>=best):
            Max = pathD
            best = pointD
        pathE = self.BFS_time(nd,velocity,turn_time, straight_time)
        pointE = self.score_estimate(pathE,velocity, turn_time, straight_time)
        print("Time : ",pointE)
        if(pointE>=best):
            Max = pathE
            best = pointE
        pathF = self.BFS_time_enhancement(nd,velocity,turn_time, straight_time)
        pointF = self.score_estimate(pathF,velocity, turn_time, straight_time)
        print("Time_enhancement : ",pointF)
        if(pointF>=best):
            Max = pathF
            best = pointF
        pathG = self.BFS_efficiency_enhancement(nd,velocity,turn_time, straight_time)
        pointG = self.score_estimate(pathG,velocity, turn_time, straight_time)
        print("Efficiency_enhancement : ",pointG)
        if(pointG>=best):
            Max = pathG
            best = pointG
        pathH = self.BFS_roadlength_enhancement(nd,velocity,turn_time, straight_time)
        pointH = self.score_estimate(pathH,velocity, turn_time, straight_time)
        print("Roadlength_enhancement : ",pointH)
        if(pointH>=best):
            Max = pathH
            best = pointH
        print("")
        print("")
        print("________________________________The chosen path____________________________")
        print("Highest point : ",best)
        print("Path sequence：")
        print("[",end="")
        for j in range(len(Max)):
            for w in range(len(tre)):
                            
                if int(Max[j].getIndex())== tre[w][0]:
                    treasure_det = 1
                    print(int(Max[j].getIndex()),end="]")
                    print("")
                    if j != len(Max)-1 :
                        print("[",end="")
                    continue
            if j == len(Max)-1 :
                ##print(int(path_sequence[j].getIndex()),end="")
                break
            
            print(int(Max[j].getIndex()),end=", ")
        return Max
    
        
        

    def strategy_2(self, nd_from, nd_to):
        return self.BFS_2(nd_from, nd_to)
