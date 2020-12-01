
#include<SoftwareSerial.h>

// TODO: return the direction based on the command you read
int ask_direction(){
    int message=-1;
    char cmd;
    if(BT.available()){cmd=BT.read();
    if(cmd=='f')message=0;
    if(cmd=='b')message=3;
    if(cmd=='r')message=1;
    if(cmd=='l')message=2;
    if(cmd=='h')message=4;
    if(cmd=='s')message=5;
    if(cmd=='e')message=6;}
    //Serial.println(message);
    return message;
}

char convert_to_hex(int x)
{
    if(x==0)return'0';
    if(x==1)return'1';
    if(x==2)return'2';
    if(x==3)return'3';
    if(x==4)return'4';
    if(x==5)return'5';
    if(x==6)return'6';
    if(x==7)return'7';
    if(x==8)return'8';
    if(x==9)return'9';
    if(x==10)return'A';
    if(x==11)return'B';
    if(x==12)return'C';
    if(x==13)return'D';
    if(x==14)return'E';
    if(x==15)return'F';
}

// TODO: send the id back by BT
void send_byte(byte *id, byte idSize)
{
    for(int i=0;i<idSize;i++)
    {
        char a=convert_to_hex(id[i]/16);
        char b=convert_to_hex(id[i]%16);
        BT.write(a);
        BT.write(b);
    }
}
