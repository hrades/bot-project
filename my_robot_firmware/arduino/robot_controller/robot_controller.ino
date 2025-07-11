#include <PID_v1.h>
// L298N H-Bridge pins
#define L298N_enA 9  
#define L298N_in2 13 
#define L298N_in1 12 
#define L298N_in3 7
#define L298N_in4 8
#define L298N_enB 11
// Encoders pins
#define right_encoder_phaseA 3
#define right_encoder_phaseB 5
#define left_encoder_phaseA 2
#define left_encoder_phaseB 4
// Encoders variables
unsigned int right_encoder_counter = 0;
unsigned int left_encoder_counter = 0;
String right_encoder_sign = "p";
String left_encoder_sign = "p";
unsigned long last_millis = 0;
const unsigned long interval = 100;
// Serial comunnication variables
bool is_right_wheel_cmd = false;
bool is_left_wheel_cmd = false;
bool is_right_wheel_forward = false;
bool is_left_wheel_forward = false;
char value[] = "00.00";
uint8_t value_idx = 0;
bool is_cmd_complete = false;
// PID variables
// Setpoint (rad/s)
double right_wheel_cmd_vel = 0.0;
double left_wheel_cmd_vel = 0.0;
// Input (rad/s)
double right_wheel_meas_vel = 0.0;
double left_wheel_meas_vel = 0.0;
// Output (0-255)
double right_wheel_cmd = 0.0;
double left_wheel_cmd = 0.0;
// Components
double Kp_r = 3.0; //11.5;
double Ki_r = 1.0; //7.5;
double Kd_r = 0.05; //0.1;
double Kp_l = 3.2; //12.8;
double Ki_l = 1.2; //8.3;
double Kd_l = 0.05; //0.1;
// Controllers
PID rightMotor(&right_wheel_meas_vel, &right_wheel_cmd, &right_wheel_cmd_vel, Kp_r, Ki_r, Kd_r, DIRECT);
PID leftMotor(&left_wheel_meas_vel, &left_wheel_cmd, &left_wheel_cmd_vel, Kp_l, Ki_l, Kd_l, DIRECT);

void setup() {
  // Set pin modes
  pinMode(L298N_enA, OUTPUT);
  pinMode(L298N_in1, OUTPUT);
  pinMode(L298N_in2, OUTPUT);
  pinMode(L298N_enB, OUTPUT);
  pinMode(L298N_in3, OUTPUT);
  pinMode(L298N_in4, OUTPUT);
  // Set Motor Rotation Direction
  digitalWrite(L298N_in1, HIGH);
  digitalWrite(L298N_in2, LOW);
  digitalWrite(L298N_in3, HIGH);
  digitalWrite(L298N_in4, LOW);
  // Set PID
  rightMotor.SetMode(AUTOMATIC);
  leftMotor.SetMode(AUTOMATIC);
  Serial.begin(115200);
  // Set encoders
  pinMode(right_encoder_phaseB, INPUT);
  pinMode(left_encoder_phaseB, INPUT);
  attachInterrupt(digitalPinToInterrupt(right_encoder_phaseA), rightEncoderCallback, RISING);
  attachInterrupt(digitalPinToInterrupt(left_encoder_phaseA), leftEncoderCallback, RISING);
}

void loop() {
  if(Serial.available()){
    char chr = Serial.read();
    if(chr == 'r'){
      is_right_wheel_cmd = true;
      is_left_wheel_cmd = false;
      value_idx = 0;
      is_cmd_complete = false;
    }
    else if(chr == 'l'){
      is_right_wheel_cmd = false;
      is_left_wheel_cmd = true;
      value_idx = 0;
    }
    else if(chr == 'p'){
      // change the direction of the rotation to positive
      if(is_right_wheel_cmd && !is_right_wheel_forward){
        digitalWrite(L298N_in1, HIGH - digitalRead(L298N_in1));
        digitalWrite(L298N_in2, HIGH - digitalRead(L298N_in2));
        is_right_wheel_forward = true;
      }
      else if(is_left_wheel_cmd && !is_left_wheel_forward){
        digitalWrite(L298N_in3, HIGH - digitalRead(L298N_in3));
        digitalWrite(L298N_in4, HIGH - digitalRead(L298N_in4));
        is_left_wheel_forward = true;
      }
    }
    else if(chr == 'n'){
      // change the direction of the rotation to negative
      if(is_right_wheel_cmd && is_right_wheel_forward){
        digitalWrite(L298N_in1, HIGH - digitalRead(L298N_in1));
        digitalWrite(L298N_in2, HIGH - digitalRead(L298N_in2));
        is_right_wheel_forward = false;
      }
      else if(is_left_wheel_cmd && is_left_wheel_forward){
        digitalWrite(L298N_in3, HIGH - digitalRead(L298N_in3));
        digitalWrite(L298N_in4, HIGH - digitalRead(L298N_in4));
        is_left_wheel_forward = false;
      }
    }
    else if(chr == ','){
      if(is_right_wheel_cmd){
        right_wheel_cmd_vel = atof(value);
      }
      else if(is_left_wheel_cmd){
        left_wheel_cmd_vel = atof(value);
        is_cmd_complete = true;
      }
      value_idx = 0;
      value[0] = '0';
      value[1] = '0';
      value[2] = '.';
      value[3] = '0';
      value[4] = '0';
      value[5] = '\0';
    }
    else{
      if(value_idx < 5){
        value[value_idx] = chr;
        value_idx++;
      }
    }
  }

  unsigned long current_millis = millis();
  if(current_millis - last_millis >= interval){

    right_wheel_meas_vel = (10 * right_encoder_counter * (60.0/374.0)) * 0.10472;
    left_wheel_meas_vel = (10 * left_encoder_counter * (60.0/374.0)) * 0.10472;

    rightMotor.Compute();
    leftMotor.Compute();
  
    if(right_wheel_cmd_vel == 0.0){
      right_wheel_cmd = 0.0;
    }
    if(left_wheel_cmd_vel == 0.0){
      left_wheel_cmd = 0.0;
    }

    String encoder_read = "r" + right_encoder_sign + String(right_wheel_meas_vel) + ",l" + left_encoder_sign + String(left_wheel_meas_vel) + ",";
    Serial.println(encoder_read);
    last_millis = current_millis;
    right_encoder_counter = 0;
    left_encoder_counter = 0;

    analogWrite(L298N_enA, right_wheel_cmd);
    analogWrite(L298N_enB, left_wheel_cmd);
  }
}

void rightEncoderCallback()
{
  if(digitalRead(right_encoder_phaseB) == HIGH){
    right_encoder_sign = "p";
  }
  else{
    right_encoder_sign = "n";
  }
  right_encoder_counter++;
}

void leftEncoderCallback()
{
  if(digitalRead(left_encoder_phaseB) == HIGH){
    left_encoder_sign = "n";
  }
  else{
    left_encoder_sign = "p";
  }
  left_encoder_counter++;
}

