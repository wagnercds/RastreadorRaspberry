# -*- coding: utf-8 -*-

import commands
import os
import time
import serial
import sys
import RPi.GPIO as GPIO
	
def writeLogConnection(errorMessage):
	try:
		arq = open("/var/log/wvdialconnect" + time.strftime("%Y%m%d")+ ".log", "a")
		arq.write(time.strftime("%Y-%m-%d %H:%M:%S") + " " + errorMessage + "\r\n")
		arq.close()
	except:
		if debug:
			print "Error :" + str(sys.exc_info()[0])
		raise
	
def verifyWvDial():
	if debug:
		print "Verificando conexão internet ..."

	ppp0 = commands.getoutput("ifconfig|grep ppp0")

	if ppp0:
		if not pingping("187.60.57.227"):
			if not pingping("www.google.com"):
				if pingping("www.microsoft.com"):
					return True	
			else:				
				return True		
		else:			
			return True
		
	if debug:	
		print "Destruindo WVdial ..."
		
	writeLogConnection("Ping Fail")

	wvdial = commands.getoutput("ps aux | pgrep wvdial")

	if wvdial:
		if debug:
			print wvdial
			print "pkill wvdial"

		os.system("pkill wvdial")
		
		writeLogConnection("Kill wvdial")

		time.sleep(7)

	return False
		
def pingping(url):
	for x in range(0, 1):
			ping = os.system("ping -c 1 " + url)
			
			if ping == 0:
				if debug:
					print "Navegando internet"				
				return True
	return False
		
def connectWvDial():
	countReset = 0	
	while not verifyWvDial():
		try:
			countReset += 1
			if debug:
				print "countReset: " + str(countReset)
			if countReset > 2:
				countReset = 0
				if debug:
					print "Reiniciando ..."
				GPIO.output(27, GPIO.LOW)
				time.sleep(5)
				GPIO.output(27, GPIO.HIGH)
				time.sleep(10)
				if debug:
					print "Reiniciado !"
				
			if debug:
				print "Conectando modem ..."
				
			port = serial.Serial ("/dev/ttyAMA0", baudrate=115200, timeout=1)
			if port.isOpen() == True:
				"""			
				if debug:
					print "Comandos de reinicialização +++"			
				port.write("+++")
				
				if debug:
					print "Time 1"
				time.sleep(1)	
				
				if debug:
					print "<enter>"
				port.write("\r\n")
				"""		
			
				port.write("AT\r\n")
				if debug:
					print "AT"
				aux = port.readline()
				writeLogConnection("AT " + aux)
			
				port.write("ATE0\r\n")
				if debug:
					print "ATE0"
				aux = port.readline()
				writeLogConnection("ATE0 " + aux)
				
				if debug:
					print "AT+IPR"
				port.write("AT+IPR=115200\r\n")
				aux = port.readline()
				writeLogConnection("AT+IPR " + aux)
				
				"""				
				if debug:
					print "AT+CFUN"
				port.write("AT+CFUN=1,1\r\n")
				aux = port.readline()		
				writeLogConnection("AT+CFUN " + aux)

				time.sleep(10)
				"""
				
				port.close()
				time.sleep(2)
				if debug:
					print "wvdial"
				os.system("wvdial &")
				writeLogConnection("Call wvdial")
				time.sleep(30)
			
				if debug:
					print "Terminou !"
			else:
				if debug:
					print "Porta serial fechada"
		except:
			if debug:
				print "Erro conexão wvdial " + str(sys.exc_info()[0])
			writeLogConnection("Error  connectWvDial " + str(sys.exc_info()[0]))
			break
		
def verifyHermes():
	if debug:
		print "Verificando conexão Hermes ..."
	hermes = commands.getoutput("ifconfig|grep ppp1")
	if hermes:
		return True
	else:
		writeLogConnection("VPN not found")
		return False
		
def connectHermes():	
	if not verifyHermes():
		if debug:
			print "Conectando hermes ..."		
		os.system("pon hermes")
		writeLogConnection("Start VPN")
		time.sleep(5)
		
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)


debug = sys.argv[1]
if debug == "False":
	debug = ""

while True:
	connectWvDial()
	connectHermes()
	time.sleep(5)
