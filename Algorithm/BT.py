from time import sleep
import serial
# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?

class bluetooth:
    def __init__(self):
        self.ser = serial.Serial()

    def do_connect(self,port):
        self.ser.close()
        #TODO: Connect the port with Serial. A clear description for exception may be helpful.
        self.ser.port=port
        self.ser.baudrate=9600
        self.ser.timeout=2
        self.ser.open()
        return True

    def disconnect(self):
        self.ser.close()

    def SerialWrite(self,output):
        send = output.encode("utf-8")
        self.ser.write(send)
        self.ser.reset_output_buffer()

    def SerialReadString(self):#for moving communication
        #TODO: Get the information from Bluetooth. Notice that the return type should be transformed into hex. 
        s=self.ser.readline().decode("utf-8")                   #byte or string ?
        self.ser.reset_input_buffer()
        return s

    def SerialReadByte(self):#for reciving RFID code
        #TODO: Get the UID from bytes. Notice that the return type should be transformed into hex.
        if self.ser.in_waiting !=0:
            key=self.ser.readline().decode('utf-8')                                  #byte only?
            self.ser.reset_input_buffer()
            return key
        return '0'
    
