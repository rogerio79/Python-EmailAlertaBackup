import os
import csv
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def abre_arquivo(arquivo) :
    aux_z = {}
    with open(arquivo) as csvarquivo:
        dataset = csv.reader(csvarquivo, delimiter='=')
        for row in dataset:
            aux_z[row[0]] = row[1]
        return aux_z

		
def envia_email():

	ultimo_arquivo = verifica_arquivo()

	conf = abre_arquivo('conf_email.csv')

	msg = MIMEMultipart()
	msg['From'] = conf['from']
	msg['To'] = conf['to']
	msg['Subject'] = conf['subject']
	message = conf['message']+' : '+ultimo_arquivo
	msg.attach(MIMEText(message))

	mailserver = smtplib.SMTP_SSL(conf['smtp_ssl'])

	# se identificando para o server
	mailserver.ehlo()

	mailserver.ehlo()

	mailserver.login(conf['login'], conf['password'])
	mailserver.sendmail(conf['from'],conf['to'],msg.as_string())

	mailserver.quit()
	
	
def getKey(item):
	return item[1]
	
	
def verifica_arquivo():	
	conf = abre_arquivo('conf_path.csv')
	
	mypath = conf['path']
	f = []
	z = []

	for (dirpath, dirnames, filenames) in os.walk(mypath):
		f.extend(filenames)
		diretorio = dirpath


	for arquivo in f:
		data = os.stat(diretorio+arquivo).st_ctime
		tamanho = os.stat(diretorio+arquivo).st_size
		z.append([arquivo, data, tamanho])

		
	z_ordenado = sorted(z, key=getKey, reverse=True) 	

	ultimo_criado, data_criado, tam_criado = z_ordenado[0]

	return ultimo_criado+', '+str(datetime.datetime.fromtimestamp(data_criado))+', '+str(tam_criado)

envia_email()

