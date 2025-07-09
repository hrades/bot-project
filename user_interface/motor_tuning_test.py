#pip install pyqt5 pyserial matplotlib --> bibliotecas necessárias

import sys
import serial
import csv
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSlider, QPushButton, QLineEdit, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RobotControl(QWidget):
    def __init__(self):
        super().__init__()

        # Serial
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

        # Dados para gráfico
        self.timestamps = []
        self.left_vels = []
        self.right_vels = []
        self.left_errors = []
        self.right_errors = []
        self.left_setpoint = 0.0
        self.right_setpoint = 0.0
        self.start_time = time.time()

        # Layout principal
        self.setWindowTitle("Controle PID com Gráficos e Ajustes")
        self.setGeometry(100, 100, 1000, 700)
        layout = QVBoxLayout()

        # Sliders de velocidade
        self.left_slider = QSlider(Qt.Horizontal)
        self.left_slider.setRange(-100, 100)
        self.left_slider.valueChanged.connect(self.send_left_command)

        self.right_slider = QSlider(Qt.Horizontal)
        self.right_slider.setRange(-100, 100)
        self.right_slider.valueChanged.connect(self.send_right_command)

        layout.addWidget(QLabel("Velocidade Roda Esquerda (-10 a 10 rad/s)"))
        layout.addWidget(self.left_slider)
        layout.addWidget(QLabel("Velocidade Roda Direita (-10 a 10 rad/s)"))
        layout.addWidget(self.right_slider)

        # Feedback
        self.left_feedback = QLabel("Vel. medida (E): 0.00 rad/s | Erro: 0.00")
        self.right_feedback = QLabel("Vel. medida (D): 0.00 rad/s | Erro: 0.00")
        layout.addWidget(self.left_feedback)
        layout.addWidget(self.right_feedback)

        # Ajuste PID
        pid_group = QGroupBox("Ajustes PID em tempo real (não envia para Arduino)")
        form_layout = QFormLayout()
        self.kp_l = QLineEdit("3.0")
        self.ki_l = QLineEdit("1.0")
        self.kd_l = QLineEdit("0.05")
        self.kp_r = QLineEdit("3.0")
        self.ki_r = QLineEdit("1.0")
        self.kd_r = QLineEdit("0.05")

        form_layout.addRow("Kp Esquerdo:", self.kp_l)
        form_layout.addRow("Ki Esquerdo:", self.ki_l)
        form_layout.addRow("Kd Esquerdo:", self.kd_l)
        form_layout.addRow("Kp Direito:", self.kp_r)
        form_layout.addRow("Ki Direito:", self.ki_r)
        form_layout.addRow("Kd Direito:", self.kd_r)
        pid_group.setLayout(form_layout)
        layout.addWidget(pid_group)

        # Gráfico
        self.figure = Figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)

        self.line_lv, = self.ax1.plot([], [], label="Velocidade Esq")
        self.line_rv, = self.ax1.plot([], [], label="Velocidade Dir")
        self.line_le, = self.ax2.plot([], [], label="Erro Esq")
        self.line_re, = self.ax2.plot([], [], label="Erro Dir")

        self.ax1.set_ylabel("Vel. (rad/s)")
        self.ax2.set_ylabel("Erro (rad/s)")
        self.ax2.set_xlabel("Tempo (s)")
        self.ax1.legend()
        self.ax2.legend()

        layout.addWidget(self.canvas)

        # Botão resetar
        reset_btn = QPushButton("Resetar Gráfico")
        reset_btn.clicked.connect(self.reset_data)
        layout.addWidget(reset_btn)

        self.setLayout(layout)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def send_left_command(self):
        val = self.left_slider.value() / 10.0
        self.left_setpoint = val
        cmd = "lp{:.2f},".format(abs(val))
        self.serial.write(b"l")
        self.serial.write(b"p" if val >= 0 else b"n")
        self.serial.write(cmd.encode())

    def send_right_command(self):
        val = self.right_slider.value() / 10.0
        self.right_setpoint = val
        cmd = "rp{:.2f},".format(abs(val))
        self.serial.write(b"r")
        self.serial.write(b"p" if val >= 0 else b"n")
        self.serial.write(cmd.encode())

    def update(self):
        if self.serial.in_waiting:
            try:
                line = self.serial.readline().decode().strip()
                if "r" in line and "l" in line:
                    t = time.time() - self.start_time
                    parts = line.split(",")
                    right = 0.0
                    left = 0.0
                    for part in parts:
                        if part.startswith("r"):
                            sign = 1 if part[1] == "p" else -1
                            right = sign * float(part[2:])
                        elif part.startswith("l"):
                            sign = 1 if part[1] == "p" else -1
                            left = sign * float(part[2:])

                    err_l = self.left_setpoint - left
                    err_r = self.right_setpoint - right

                    # Armazenar
                    self.timestamps.append(t)
                    self.left_vels.append(left)
                    self.right_vels.append(right)
                    self.left_errors.append(err_l)
                    self.right_errors.append(err_r)

                    # Atualizar gráfico
                    self.line_lv.set_data(self.timestamps, self.left_vels)
                    self.line_rv.set_data(self.timestamps, self.right_vels)
                    self.line_le.set_data(self.timestamps, self.left_errors)
                    self.line_re.set_data(self.timestamps, self.right_errors)

                    self.ax1.relim()
                    self.ax1.autoscale_view()
                    self.ax2.relim()
                    self.ax2.autoscale_view()
                    self.canvas.draw()

                    # Atualizar feedback
                    self.left_feedback.setText(f"Vel. medida (E): {left:.2f} rad/s | Erro: {err_l:.2f}")
                    self.right_feedback.setText(f"Vel. medida (D): {right:.2f} rad/s | Erro: {err_r:.2f}")

            except Exception as e:
                print("Erro:", e)

    def reset_data(self):
        self.timestamps.clear()
        self.left_vels.clear()
        self.right_vels.clear()
        self.left_errors.clear()
        self.right_errors.clear()
        self.start_time = time.time()

    def closeEvent(self, event):
        # Salvar CSV
        with open("velocidade_erro_log.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Tempo", "Vel_E", "Vel_D", "Erro_E", "Erro_D"])
            for i in range(len(self.timestamps)):
                writer.writerow([
                    f"{self.timestamps[i]:.2f}",
                    f"{self.left_vels[i]:.2f}",
                    f"{self.right_vels[i]:.2f}",
                    f"{self.left_errors[i]:.2f}",
                    f"{self.right_errors[i]:.2f}"
                ])
        self.serial.close()
        print("Dados salvos em 'velocidade_erro_log.csv'")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RobotControl()
    window.show()
    sys.exit(app.exec_())
