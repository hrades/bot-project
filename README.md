# 🏎️💨 Robot Project

![Badge de Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)

Desenvolvimento de um projeto de robô móvel autônomo com ROS2

## 📋 Índice
- [📁 Pastas](#pastas)
- [🛠️ Tecnologias Utilizadas](#tecnologias-utilizadas)
- [💡 Sobre o Projeto](#sobre-o-projeto)

---

## Pastas
- [my_robot_bringup](#my_robot_bringup): Arquivos para inicializar o robô por completo (com todas as configurações de controle)
- **my_robot_description**: Arquivos de construção e visualização do robô (rviz e gazebo)
- **my_robot_firmware**: Arquivos de teste para Arduino + Interface e controlador PID
- [sllidar_ros2](#sllidar_ros2): Driver do LiDAR adaptado deste repositório -> https://github.com/Slamtec/sllidar_ros2
- **user_interface**: Programas de auxílio visual para testes

## Tecnologias Utilizadas
- **Linguagem pyhton 🐍**
- **Linguagem C++ e arduino 👨🏻‍💻**
- **ROS2 🤖**
- **Arquivos URDF e XACRO ⚙️**
- **Gazebo Classic 📦**

---

## Sobre o Projeto

Este projeto tem como objetivo a criação de um robô móvel autônomo utilizando ROS2 (Humble), Linux (Ubuntu 22.04) e RaspberryPi, visando a simulação e construção de protótipos reais. Ele está relacionado com o projeto de conclusão de curso de Engenhara de Controle e Automação.
Esta branch "gz-classic" utiliza o Gazebo Clássico para a simulação do robô.

- Siga as seguintes instruções para [instalar o ROS2](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html#install-ros-2-packages).

Para este projeto, devem ser instalados os seguintes pacotes do ros2:
```bash
sudo apt install ros-humble-gazebo* 
sudo apt install ros-humble-ros2-control 
sudo apt install ros-humble-ros2-controllers 
sudo apt install ros-humble-xacro 
sudo apt install ros-humble-joint-state-publisher-gui 
sudo apt install ros-humble-turtlesim (opcional) 
sudo apt install ros-humble-robot-localization
sudo apt install ros-humble-twist-mux
sudo apt install ros-humble-joy 
sudo apt install ros-humble-joy-teleop
sudo apt install ros-humble-teleop-twist-joy
sudo apt install ros-humble-teleop-twist-keyboard
sudo apt install ros-humble-tf-transformations 
sudo apt install ros-humble-tf2-tools 
sudo apt install ros-humble-urdf-tutorial 
sudo apt install ros-humble-navigation2  
sudo apt install ros-humble-nav2-bringup 
```
E do python:
```bash
sudo apt python3-pip
pip install pyserial
pip install transforms3d
```
Quando tudo estiver configurado, crie uma pasta chamada "robot_ws/src" e baixe este repositório no computador e na raspberry pi
```bash
mkdir robot_ws/src
git clone https://github.com/hrades/bot-project.git
```
Depois de baixar, navegue até "robot_ws" e execute o comando de construção:
```bash
cd /robot_ws/
colcon build
```
Se o comando não for encontrado, [instale colcon](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html#install-colcon) antes e rode o comando novamente.
Caso haja problemas com o comando, utilize para cada pacote:
```bash
colcon build --packages-select <nome_do_pacote>
```
Sempre que abrir um novo terminal, rode:
```bash
source install/setup.bash
```

## my_robot_bringup
Segue o passo a passo de como simular o robô, utilizando o computador apenas. Cada etapa deve ser feita em um novo terminal.

- Para rodar a simulação
```bash
ros2 launch my_robot_bringup my_gazebo_simu.launch.xml
```
- Para controlar o robô virtual com controle de video-game
```bash
ros2 launch my_robot_bringup joystick.launch.py
```
- Para inicializar navegação autônoma
```bash
ros2 launch my_robot_bringup online_async_launch.py
```
```bash
ros2 launch my_robot_bringup navigation_launch.py
```

## sllidar_ros2
Disponibilização do driver já adaptado para o RPLiDAR C1 da SLAMTEC, que está sendo utilizado neste projeto. Deve ser implementado na raspberry pi.

- Para baixar o repositório original, que contém outros LiDARs:
```bash
git clone https://github.com/Slamtec/sllidar_ros2.git
```
