#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫
/* pin---- SDA:9 SCK:13 MOSI:11 MISO:12 GND:GND RST:9  */

byte* rfid(byte* idSize) {
    // 確認是否有新卡片
  
    //Serial.println("in rfid");
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      byte *id = mfrc522.uid.uidByte;   // 取得卡片的UID
      *idSize = mfrc522.uid.size;   // 取得UID的長度
//      *idSize = 4;
     // Serial.print("PICC type: ");      // 顯示卡片類型
      // 根據卡片回應的SAK值（mfrc522.uid.sak）判斷卡片類型
      MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
      //Serial.println(mfrc522.PICC_GetTypeName(piccType));

      /*Serial.print("UID Size: ");       // 顯示卡片的UID長度值
      Serial.println(mfrc522.uid.size);
      Serial.println(sizeof(mfrc522.uid.size));

      if (id[0]==169)
      {Serial.print("success");}  //得到寶藏
  *   
      for (byte i = 0; i < *idSize; i++) {  // 逐一顯示UID碼
        Serial.print("id[");
        Serial.print(i);
        Serial.print("]: ");
        Serial.println(id[i], HEX);       // 以16進位顯示UID值  
      }
      
      Serial.println();*/

      mfrc522.PICC_HaltA();  // 讓卡片進入停止模式
      return id;
    }
    return -1;
}
