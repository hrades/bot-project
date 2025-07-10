// L298N pins
#define L298N_enA 9  
#define L298N_in2 13 
#define L298N_in1 12 

// Encoder pins  
#define ENCODER_A 5   //interrupt pin

volatile unsigned int encoder_count = 0;

void setup() {

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  pinMode(ENCODER_A, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENCODER_A), countPulse, RISING);

  Serial.begin(57600);

  Serial.println("Iniciando contagem de pulsos por 30 segundos...");

  analogWrite(ENA, 255);
}

void loop() {
  static bool contando = true;
  static unsigned long start_time = millis();

  if (contando && millis() - start_time >= 100000) {
    analogWrite(ENA, 0);  // Para o motor
    Serial.print("Total de pulsos em 1 minuto: ");
    Serial.println(encoder_count);
    contando = false;
  }
}

void countPulse() {
  encoder_count++;
}

