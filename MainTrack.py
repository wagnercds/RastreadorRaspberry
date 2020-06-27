# -*- coding: utf-8 -*-
import serial
import urllib2
import urllib
import socket
import sys
import time
import RPi.GPIO as GPIO

"""
GPIO 04 Bloqueio 
	0 - Desbloqueado
	1 - Bloqueado
	
GPIO 18 Pós-chave
	0 - Chave Ligada
	1 - Chave desligada	
"""

def writeLogConnection(errorMessage):
	try:
		arq = open("/var/log/MainTrack" + time.strftime("%Y%m%d")+ ".log", "a")
		arq.write(time.strftime("%Y-%m-%d %H:%M:%S") + " " + errorMessage + "\r\n")
		arq.close()
	except:
		if debug:
			print "Error :" + str(sys.exc_info()[0])
		raise

def debugMessage(message):
	if debug:
		print message
		
def sendMessage(message):
	debugMessage(gpsLine)	
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
		sock.sendto(message, ("187.60.57.227", 15001))
		debugMessage("Enviado !")		
	except:		
		debugMessage("Erro ao enviar: " + str(sys.exc_info()[0]))
		writeLogConnection("Error send position " + str(sys.exc_info()[0]))
		raise

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SerialNumber = "LAB001"
portGPS = serial.Serial ("/dev/ttyUSB1", baudrate=38400, timeout=1)
#portGPS = serial.Serial ("/dev/ttyUSB0", baudrate=9600, timeout=1)

countGPS = 0

gpsLine = ""

countPosChave = 0

GPIO.output(4, GPIO.HIGH)

debug = sys.argv[1]
if debug == "False":
	debug = ""
		
while True:
	try:
		#debugMessage("Lendo Porta Serial")
		gpsLine = portGPS.readline()			
		#debugMessage(gpsLine)	
		#debugMessage("Dados lido !")

		debugMessage("Chave: " + str(GPIO.input(18)))
		debugMessage("Bloqueio: " + str(GPIO.input(4)))
		
		# Verifica se passou um minuto antes de enviar a posição
		if "GPRMC" in gpsLine:		
			countGPS += 1		
			debugMessage("CountGPS: " + str(countGPS))
			if countGPS > 60:			
				debugMessage("Enviando ...")
				countGPS = 0
				sendMessage(gpsLine + "," + SerialNumber + "," + str(GPIO.input(18)) + "," + str(GPIO.input(4)))
			
			# Verifica se o pós-chave foi desligado			
			if GPIO.input(18) == 1 and GPIO.input(4) == 0:
				debugMessage("Contador poschave: " + str(countPosChave))
				countPosChave += 1			
				if countPosChave > 60:
					debugMessage("Veiculo bloqueado !")				
					GPIO.output(4, GPIO.HIGH)
					countPosChave = 0
			else:
				debugMessage("Zera Contador Bloqueio")			
				countPosChave = 0
				
		if "$" not in gpsLine:
			debugMessage("Sem leitura GPS")
			writeLogConnection("GPS is not ready")
	except:
		if debug:
			print "Error while " + str(sys.exc_info()[0])
		writeLogConnection("While error " + str(sys.exc_info()[0]))