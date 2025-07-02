//L298N pins
#define enA 9
#define in1 12
#define in2 13
//encoder pins
#define encA 3
#define encB 5

unsigned encA_counter = 0;
String encoder_sign = "p";
double wheel_vel = 0.0; //must be rad/s

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(encB, INPUT);

  attachInterrupt(digitalPinToInterrupt(encA), encoderCallback, RISING);

  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}

void loop() {
  wheel_vel = 10* encA_counter * (60.0/385.0) * 0.10472; //transformation rpm to rad/s
  String encoder_read = encoder_sign + String(wheel_vel);
  Serial.println(encoder_read);
  analogWrite(enA, 100);

  encA_counter = 0;
  delay(100);
}

void encoderCallback(){
  encA_counter++;
  if(digitalRead(encB)==HIGH){
    encoder_sign = "p";
  }
  else{
    encoder_sign = "n";
  }
}