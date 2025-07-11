#define ENA 9
#define IN1 12
#define IN2 13

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  Serial.begin(115200);
  Serial.println("Comandos: f <velocidade>, b <velocidade>, s");
}

void limparBufferSerial() {
  while (Serial.available()) {
    Serial.read();
  }
}

void loop() {
  if (Serial.available()) {
    char comando = Serial.read();
    int velocidade = 0;

    if (comando == 'f' || comando == 'b') {
      while (Serial.available() == 0); // espera o próximo caractere
      if (Serial.read() == ' ') {
        while (Serial.available() == 0);
        velocidade = Serial.parseInt(); // Lê o valor de velocidade
      }
    }

    switch (comando) {
      case 'f':
        analogWrite(ENA, velocidade);
        Serial.print("Motor para frente com velocidade ");
        Serial.println(velocidade);
        break;

      case 'b':
        analogWrite(ENA, -velocidade);
        Serial.print("Motor para trás com velocidade ");
        Serial.println(velocidade);
        break;

      case 's':
        analogWrite(ENA, 0);
        Serial.println("Motor parado");
        break;

      default:
        Serial.println("Comando inválido. Use: f <0-255>, b <0-255>, s");
        break;
    }

    limparBufferSerial(); // limpa qualquer caractere restante no buffer
  }
}

