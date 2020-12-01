import BT
import maze
#import score

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)

class interface:
    def __init__(self):
        print("")
        print("Arduino Bluetooth Connect Program.")
        print("")
        self.ser = BT.bluetooth()
        port = input("PC bluetooth port name: ")
        while(not self.ser.do_connect(port)):
            if(port == "quit"):
                self.ser.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
        input("Press enter to start.")
        self.ser.SerialWrite('s')

    def wait_for_node(self):
        return self.ser.SerialReadByte()

    def send_action(self,dirc):
        if(dirc == maze.Action.ADVANCE):
            self.ser.SerialWrite('f')
        elif(dirc == maze.Action.U_TURN):
            self.ser.SerialWrite('b')
        elif(dirc == maze.Action.TURN_RIGHT):
            self.ser.SerialWrite('r')
        elif(dirc == maze.Action.TURN_LEFT):
            self.ser.SerialWrite('l')
        elif(dirc == maze.Action.HALT):
            self.ser.SerialWrite('h')
        else:
            print ('Error: An invalid input for action.')

    def end_process(self):
        self.ser.SerialWrite('e')
        self.ser.disconnect()
