// dir = 0 : advance
// dir = 1 : left
// dir = 2 : right
// dir = 3 : back



// TODO: determine the behavior of each port when occuring a node(here represented as an integer)
//#include"track.h"
#include <Wire.h>
extern int r2,r1,m,l1,l2;   //extern?

void node(int dir){
    switch(dir){
        case 0:
            MotorWriting(150,200);
            delay(250);
            tracking(r2,r1,m,l1,l2);break;
        
        case 1: //turn right
            MotorWriting(150,150);
            delay(400);
            MotorWriting(0,0);
            delay(2000);
            MotorWriting(-,200);
            delay(180);
             MotorWriting(0,0);
            delay(2000);
            
            while(r1==0){
              MotorWriting(-100,100);
            }
           
            MotorWriting(0,0);
            delay(2000);
            MotorWriting(100,100);
            delay(100);break;
            
            
        
        case 2: //turn left
            MotorWriting(150,150);
            delay(400);
            MotorWriting(0,0);
            delay(2000);
            MotorWriting(200,-200);
            delay(180);
            MotorWriting(0,0);
            delay(2000);
            
            while(l1==0){
              MotorWriting(100,-100);
            }
            
            MotorWriting(0,0);
            delay(2000);
            MotorWriting(100,100);
            delay(100);break;
            
        case 3: //180
            //MotorWriting(255,255);
            //delay(1000);
            MotorWriting(-255,255);
            delay(400);
             MotorWriting(0,0);
            delay(2000);
            while(m==0){
              MotorWriting(-100,100);
            }
             MotorWriting(0,0);
            delay(2000);
           break;
            
        case 4://halt
            MotorWriting(0,0);
            delay(2000);break;


    }

}


