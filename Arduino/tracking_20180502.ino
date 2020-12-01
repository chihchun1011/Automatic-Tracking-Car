#include<SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>  

 
#define RST_PIN      2        // RFID resetpin
#define SS_PIN       4       // RFID selection pin
MFRC522 mfrc522(SS_PIN, RST_PIN);
SoftwareSerial BT(8,7);   //bluetooth RX,TX


#define MotorL_I1     A5  //定義 I1 接腳（左）
#define MotorL_I2     6  //定義 I2 接腳（左）
#define MotorR_I3     9 //定義 I3 接腳（右）
#define MotorR_I4     10 //定義 I4 接腳（右）
#define MotorL_PWML   3  //定義 ENA (PWM調速) 接腳
#define MotorR_PWMR    5  //定義 ENB (PWM調速) 接腳
// 循線模組
#define R2  A0  // Define Second Right Sensor Pin
#define R1  A1  // Define First Right Sensor Pin
#define M   A2  // Define Middle Sensor Pin
#define L1  A3  // Define First Left Sensor Pin
#define L2  A4  // Define Second Leftt Sensor Pin

enum ControlState {
   START_STATE,
   REMOTE_STATE,
};
ControlState _state=START_STATE;
void Remote_Mode();
void Start_Mode();
void SetState();
int _cmd=0;

void setup()
{
    BT.begin(9600); //bluetooth initialization
    #ifndef DEBUG
    #define DEBUG
    Serial.begin(9600);
    #endif
    SPI.begin();         //RFID initialization
    mfrc522.PCD_Init();
    pinMode(MotorL_I1,   OUTPUT);
   pinMode(MotorL_I2,   OUTPUT);
   pinMode(MotorR_I3,   OUTPUT);
   pinMode(MotorR_I4,   OUTPUT);
   pinMode(MotorL_PWML, OUTPUT);
   pinMode(MotorR_PWMR, OUTPUT);
   pinMode(R1, INPUT); 
   pinMode(R2, INPUT);
   pinMode(M,  INPUT);
   pinMode(L1, INPUT);
   pinMode(L2, INPUT);
    /*define your pin mode*/
   
}

#include "track.h"
//#include "node.h"
#include "bluetooth.h"
#include "RFID.h"
int r2=0,r1=0,m=0,l1=0,l2=0;
    int dir=4;
    int _Tp=80;
    byte* a=NULL;
    byte* b=NULL;
void loop()
{
   if(_state == START_STATE) Start_Mode();
   else if(_state == REMOTE_STATE) Remote_Mode();
   SetState(); 
   
}

void SetState() {
  _cmd=ask_direction();
  if(_state==START_STATE){
      if(_cmd==5){
        _state= REMOTE_STATE; }
      else _state=_state;
  }
  else if(_state==REMOTE_STATE){
      if(_cmd==6){
        _state=START_STATE;
      }
      else _state=_state;
  }
 
}

void Start_Mode(){
  MotorWriting(0,0);
}
void Remote_Mode(){
     r1 = digitalRead(R1); // right-outer sensor
     r2 = digitalRead(R2); // right-inner sensor
      m = digitalRead(M); // middle sensor
     l2 = digitalRead(L1); // left-inner sensor
     l1= digitalRead(L2); // left-outer sensor   
  if((r1==1 && m==1 && l1==1)||(r2==1 && l2==1)||(r1==1 && m==1 && l2==1)||(r2==1 && m==1 && l1==1)){
    node(4);
    MotorWriting(150,150);//直走
    delay(300);
    MotorWriting(0,0);//直走
    //delay(250);
    //Serial.println(mfrc522.PICC_IsNewCardPresent());
    
     a=rfid(b);
      //Serial.println("has rfid");
      send_byte(a,4);
      //else BT.write('y');
 
    dir=-1;
    while(dir==-1){
      dir=ask_direction();
    }
    //Serial.println(dir);
    node(dir);
    
  } 
   else{
    tracking(r2,r1,m,l1,l2);
   
  }
} 
void node(int dir){
    switch(dir){
        case 0:
           //MotorWriting(150,100);//直走
           //delay(150);
           MotorWriting(0,0);//直走
           delay(250);break;
           //tracking(r2,r1,m,l1,l2);
        
        case 1: //turn right
            
            
            MotorWriting(150,150);
           // Serial.print("1st");
           delay(80);
            MotorWriting(-80,0);//轉彎(小)
            delay(320);
            //MotorWriting(0,0);
            // Serial.print("2nd");
           // delay(2000);
            //Serial.print(digitalRead(R1));
            //轉到偵測到黑
            while(digitalRead(L1) ==0){
             // Serial.print("white");
              MotorWriting(-60,0);
            }
           
            MotorWriting(0,0);
            //Serial.print("3rd");
            delay(500);
            MotorWriting(100,100);//直走小(可嘗試刪掉)
            delay(100);break;
            
            
        
        case 2: //turn left
            MotorWriting(150,150);
            //delay(250);
            //MotorWriting(0,0);
            delay(80);
            MotorWriting(0,-80);
            delay(320);
            MotorWriting(0,0);
            //delay(2000);
            
            while(digitalRead(R1)==0){
              MotorWriting(0,-60);
            }
            
            MotorWriting(0,0);
            delay(500);
            MotorWriting(100,100);
            delay(100);break;
            
        case 3: //180
            MotorWriting(90,90);
            delay(100);
           
            MotorWriting(0,0);
            MotorWriting(-90,90);
            delay(400);
             MotorWriting(0,0);
            delay(200);
            while(digitalRead(L1)==0){
              MotorWriting(-50,50);
            } 
             MotorWriting(0,0);
           delay(100);
           break;
            
        case 4://halt
            MotorWriting(0,0);
            delay(100);break;
            


    }

}




