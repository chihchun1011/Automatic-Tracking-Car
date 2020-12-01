// TODO: Write the functions from what you learned in former labs.

#include <SoftwareSerial.h>
#include <Wire.h>
#define DEBUG

int extern _Tp;


void MotorInverter(int motor, bool& dir) {
    
    if(motor==MotorL_PWML){
        if(dir){
            digitalWrite(MotorL_I1,HIGH);
            digitalWrite(MotorL_I2,LOW);
        }
        else{
            digitalWrite(MotorL_I1,LOW);
            digitalWrite(MotorL_I2,HIGH);
        }
    }
    if(motor==MotorR_PWMR){
        if(dir){
            digitalWrite(MotorR_I3,HIGH);
            digitalWrite(MotorR_I4,LOW);
        }
        else{
            digitalWrite(MotorR_I3,LOW);
            digitalWrite(MotorR_I4,HIGH);
        }
    }
}

void MotorWriting(double vR, double vL) {
    bool R_dir,L_dir;
    if(vR<0)
    {
        R_dir=false;
        vR=-vR;
    }
    else R_dir=true;
    //Serial.println(vL);
    if(vL<0)
    {
        L_dir=false;
        vL=-vL;
        
    }
    else L_dir=true;
    MotorInverter(MotorR_PWMR,R_dir);
    MotorInverter(MotorL_PWML,L_dir);
    analogWrite(MotorL_PWML,vL);
    analogWrite(MotorR_PWMR,vR);
    //Serial.println(vL);
    
}


void tracking(int r2,int r1,int m,int l1,int l2){    //main velocity
                      // Velocity of Car
 /* double _w2=10.0 ;                       // Weight Value for the Outer Sensor
  double _w1=_w2/2.0 ;                   // Weight Value for the Inner Sensor
  double _Kp=60 ;                       // _Kp Parameter
  double _Kd=0.03 ;                        // _Kd Parameter
  double _Ki=6.0 ;                         // _Ki Paramete  
  double _integral=0 ; */  
  
    double _w2=10;
    double _w1=_w2/2.0;
    double _Kp=9;
    double error=r2*_w2+r1*_w1+l1*(-_w1)+l2*(-_w2);
    if ((r1+r2+l1+l2)>0) error/=(r1+r2+l1+l2);
    error*=_Kp;
    MotorWriting((_Tp+error), _Tp-error); 
  /* double error=_w2*l2+_w1*l1-_w2*r2-_w1*r1;           
    if((l1+l2==2)||(l1+m==2)||(r1+m==2)||(r1+r2==2))error=error/2; 
    double revise = 4/5;                                           //need to test
    _integral = revise*_integral + error;      
    if(error>=1.5) _Tp=0;      
    double power=_Kp*error + _Ki*_integral;
    double vR=_Tp+power;
    double vL=_Tp-power; 
    MotorWriting((int)vR, (int)vL);  */ 
}



