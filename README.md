# RastreadorRaspberry
Scripts para um rastreador veicular usando Raspberry e Python

Ele é composto por três scripts 

- *MainTrack.py*: Responsável por monitorar se o veículo está ligado, bloquear o veículo, receber comandos via TCP e receber os sinais do GPS;

- *powerOff.py*: Script para desligar a placa;

- *wdialconnect.py*: Script para fazer a conexão com um modem GSM (ou qualquer um que aceite comandos AT)

Todos esses scripts devem ser configurados como serviços no Raspberry (ou qualquer equipamento que tenha um interpretador Python)
