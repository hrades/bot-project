# 🏎️💨 Robot Project

![Badge de Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)

Desenvolvimento de um projeto de robô móvel autônomo com ROS2

## 📋 Índice
- [📁 Pastas](#pastas)
- [🛠️ Tecnologias Utilizadas](#tecnologias-utilizadas)
- [💡 Sobre o Projeto](#sobre-o-projeto)
- [⚙️ Configurações do sistema](#configurações-do-sistema)
- [🤖 Robot Setup](#robot-setup)

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

---

## Configurações do Sistema

- [Memória SWAP](#memória-swap)
- [ROS2 e dependências](#baixar-ros2-e-dependências)
- [Udev Rules](#udev-rules)

### Memória SWAP
Caso a raspberry pi tenha pouca memória RAM, recomenda-se configurar uma memória swap no cartão micro SD. Crie um arquivo com o comando a seguir, e coloque o nome da sua área de trabalho onde estiver `<ws>`
```bash
sudo fallocate -l 4G /home/<ws>/swapfile
sudo chmod 600 /home/<ws>/swapfile
sudo mkswap /home/<ws>/swapfile
```
Com esses comandos, a memória swap estará criada e convertida. Ative e verifique com os comandos a seguir:
```bash
sudo swapon /home/<ws>/swapfile
sudo swapon --show
```
Edite o arquivo `fstab`, adicionando `/home/<ws>/swapfile swap swap defaults 0 0` à última linha. Para abrir e editar o arquivo, use o comando:
```bash
sudo nano /etc/fstab
```
Salve apertando 'Ctrl+O' e saia do arquivo com 'Ctrl+X'. Por fim, reinicie o sistema:
```bash
sudo reboot
```

### Baixar ROS2 e dependências

Siga as seguintes instruções para [instalar o ROS2](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html#install-ros-2-packages) tanto na sua máquina como na raspberry pi.
Quando finalizar a instalação, rode o seguinte comando no seu terminal:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

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
sudo apt install libserial-dev
```
E do python:
```bash
sudo apt install python3-pip
pip install pyserial
pip install transforms3d
```
Quando tudo estiver configurado, crie uma pasta chamada "robot_ws/src" e baixe este repositório no computador e na raspberry pi
```bash
mkdir robot_ws/src
git clone https://github.com/hrades/bot-project.git
```
Apague os pacotes desse repositório que não fazem parte da lógica do ROS. A disposição deve ficar assim:
```bash
src
  |_ my_robot_bringup
  |_ my_robot_description
  |_ my_robot_firmware
  |_ sllidar_ros2
```
Para apagar, utilize o comando:
```bash
rm -rf <nome_da_pasta1> <nome_da_pasta2> ...
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
Sempre que abrir um novo terminal, rode no workspace do projeto:
```bash
source install/setup.bash
```

### Udev Rules
- Regras para as portas seriais reconhecerem o arduino e o LiDAR

Acesse a pasta de regras:
```bash
cd /etc/udev/rules.d
```
Crie uma nova regra:
```bash
sudo touch 90-fesabot.rules
```
Abra o arquivo em modo edição:
```bash
sudo nano 90-fesabot.rules
```
Cole o código a seguir. Salve com 'Ctrl+O' e saia com 'Crtl+X'
```bash
KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE:="0777", SYMLINK+="rplidar"
SUBSYSTEM=="tty", GROUP="plugdev". MODE="0660"
SUBSYSTEMS=="usb", ATTRS{idProduct}=="7523", ATTRS{idVendor}=="1a86", SYMLINK+="arduino"
```
Caso o idVendor e o idProduct sejam diferentes, conecte, um de cada vez, o arduino e o LiDAR e rode o comando `lsusb` para encontrar as informações.
Após salvar o arquivo, reinicie as regras udev:
```bash
sudo udevadm control --reload-rules && sudo service udev restart && sudo udevadm trigger
```
Para verificar se ocorreu corretamente, acesse a pasta /dev `(cd /dev)`, utilize o comando `ls` e procure pelos nomes "arduino" e "rplidar".
Você também pode conectar os dispositivos e checar as portas com:
```bash
ls -l /dev | grep ttyUSB
```

---

## Robot Setup

**Configurações de hardware**

### Montagem

Necessário possuir todos os materiais fabricados da pasta 'componentes fisicos'

1. Com porcas e parafusos de 3,5 mm, monte os suportes dos motores na base
2. Monte os motores nos suportes. Eles devem ficar "embaixo" da base
3. Monte o acoplamento e a roda de cada motor em seu eixo
4. Monte o topo da base impressa do LiDAR em seu suporte impresso. Utilize parafusos ou cola quente
5. Junte o LiDAR ao seu suporte com fitas dupla face forte
6. Siga a imagem abaixo para alocar os demais [componentes](https://github.com/hrades/bot-project/blob/gz-classic/componentes%20fisicos/BOM-robo.xlsx) e fixá-los com fita dupla face forte

![Robo-montado](https://github.com/hrades/bot-project/blob/gz-classic/pictures/robo-componentes.png "Robo-montado")  

### Arduino Nano

Abra o arquivo 'robot_controllerV2.ino', que está na pasta '/my_robot_firmware/arduino/robot_controller' no [ArduinoIDE](https://www.arduino.cc/en/software)  
Adapte o código, como os parâmetros PID e os pinos, caso necessário. Recomenda-se manter o padrão de conexões sugeridos.  

#### Conexões elétricas
Conecte os fios dos motores na Ponte-H L298N seguindo o padrão abaixo:  
![Ponte-H](https://github.com/hrades/bot-project/blob/gz-classic/pictures/conexoes-ponteH.png "Ponte-H")  
Realize as seguintes conexões para o Arduino Nano:  
![Arduino Nano](https://github.com/hrades/bot-project/blob/gz-classic/pictures/conexoes-arduino.png "Arduino Nano")  
Conecte o Arduino Nano à Raspberry Pi via USB

### Raspberry

Conecte o LiDAR, o Arduino Nano e a câmera na Raspberry Pi.  
  
Para alimentar a Raspberry Pi, pode-se utilizar um conversor DC macho 2,1x5,5mm ou um cabo micro-USB adaptado.  
- Adapte seu cabo micro-USB abrindo-o e deixando os fios vermelho (fase) e preto (neutro) à mostra, cortando os demais.

Conversor DC-DC
- Utilizado para converter 12V da fonte para 5V a serem utilizados pela Raspberry Pi e pelo Arduino Nano
- Faça uma solda baseando-se na imagem a seguir:
![DC-DC](https://github.com/hrades/bot-project/blob/gz-classic/pictures/DC-DC.png "DC-DC")
- Com um multímetro, meça o terminal de saída após aplicar 12V na estrada e gire o pino até a tensão chegar a 5V
- Desconecte o multímetro e solde um fio do cabo microe-USB em cada terminal de saída. Conecte-o na Raspberry
- Solde um jumper em cada terminal de saída e conecte-os ao Arduino Nano

---

## my_robot_bringup
Segue o passo a passo de como simular o robô, utilizando o computador apenas. Cada etapa deve ser feita em um novo terminal.

- Para rodar a simulação
```bash
ros2 launch my_robot_bringup my_gazebo_simu.launch.xml
```
Se o gazebo apresentar erros com o controller_manager, realize os passos a seguir:
```bash
# Baixe a nova chave GPG
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Atualize o repositório com a nova chave
echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Atualize os índices
sudo apt update
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
