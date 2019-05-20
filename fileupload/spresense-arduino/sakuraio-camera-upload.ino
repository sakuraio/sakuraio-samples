#include <Camera.h>
#include <SakuraIO.h>
#include <Wire.h>

//SakuraIO_SPI sakuraio(10);
SakuraIO_I2C sakuraio;


void setup() {
  delay(1000);
  Serial.begin(115200);

  theCamera.begin();
  theCamera.setAutoWhiteBalanceMode(CAM_WHITE_BALANCE_DAYLIGHT);

  theCamera.setStillPictureImageFormat(
     CAM_IMGSIZE_VGA_H,
     CAM_IMGSIZE_VGA_V,
     CAM_IMAGE_PIX_FMT_JPG);

  Wire.setClock(100000);
  Wire.begin();
  delay(3000);
 
  Serial.print("Waiting to come online");
  for(;;){
    if( (sakuraio.getConnectionStatus() & 0x80) == 0x80 ) break;
    Serial.print(".");
    delay(1000);
  }
  Serial.println("");
}


uint8_t sakuraioSend(){
  uint8_t ret;
  
  ret = sakuraio.send();
  if (ret != CMD_ERROR_NONE) return ret;
  
  while(1){
    uint8_t queue, immediate;
    uint8_t ret = sakuraio.getTxStatus(&queue, &immediate);
    if (ret == CMD_ERROR_NONE){
      if(queue == 0x00){
        delay(1);
      }else if(queue == 0x02){
        return 0x00;
      }else if(queue == 0x01){
        return CMD_ERROR_NONE;
      }
    }
  }
  return 0x00;
}

uint8_t startUpload(uint32_t size){
  uint8_t ret;
  
  ret = sakuraio.clearTx();
  if (ret != CMD_ERROR_NONE) return ret;
  
  ret = sakuraio.enqueueTx((uint8_t)1, (uint32_t)size);
  if (ret != CMD_ERROR_NONE) return ret;

  return sakuraioSend();
}

uint8_t sendChunk(uint32_t sequence, uint8_t *data, uint32_t size){
  uint8_t ret;
  
  ret = sakuraio.clearTx();
  if (ret != CMD_ERROR_NONE) return ret;

  ret = sakuraio.enqueueTx((uint8_t)2, sequence);
  if (ret != CMD_ERROR_NONE) return ret;
  
  for(uint8_t i=0; i<size; i+=8){
    ret = sakuraio.enqueueTx((uint8_t)0, data+i);
    if (ret != CMD_ERROR_NONE) return ret;
  }

  return sakuraioSend();
}

uint8_t finishUpload(){
  uint8_t ret;

  ret = sakuraio.clearTx();
  if (ret != CMD_ERROR_NONE) return ret;
 
  ret = sakuraio.enqueueTx((uint8_t)3, (uint32_t)0);
  if (ret != CMD_ERROR_NONE) return ret;

  return sakuraioSend();
}

void loop() {
  Serial.println("call takePicture()");
  CamImage img = theCamera.takePicture();
  
  uint32_t start = millis();

  uint8_t *_photo_jpg = img.getImgBuff();
  uint32_t len = (uint32_t)img.getImgSize();
  Serial.print("Size=");
  Serial.println(len);

  while(startUpload(len) != CMD_ERROR_NONE){
    delay(100);
  }

  uint8_t data[8*15];

  for(uint32_t index=0; index<len; index+=8*15) {
    uint8_t ret = 0;
    while(ret != CMD_ERROR_NONE){
      uint32_t size = 8*15;
      if(size > len-index){
        size = len-index;
      }
      Serial.print("Chunk sequence=");
      Serial.print(index/(8*15));
      Serial.print(" index=");
      Serial.print(index);
      Serial.print(" size=");
      Serial.println(size);
  
      memcpy_P(data, &(_photo_jpg[index]), size);
      ret = sendChunk(index/(8*15), data, size);
      if(ret != CMD_ERROR_NONE){
        Serial.println("Retry");
      }
    }
  }

  while(finishUpload() != CMD_ERROR_NONE){
    delay(100);
  }

  uint32_t time = millis() - start;
  Serial.println(time);

  delay(5000);
}
