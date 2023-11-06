#!/usr/bin/python3
import configparser
from datetime import datetime
from Mailer import Mailer
from time import sleep
from os import path

def error(error) -> None:
	mailer = Mailer()
	mailer.addSubject(f"[Veeam] Fehlgeschlagen") 
	mailer.addError(f"{error}")
	mailer.sendMail()
	raise ValueError(error)

config = configparser.ConfigParser()
config.read("config.ini")
veeam_lockfile_path = config['VEEAM']['veeam-lockfiles']
backup_lockfile_path = f"{config['BACKUP']['backup-destination']}/{config['BACKUP']['backup-lockfile-path']}"
wait_for_backup_minutes = int(config['VEEAM']['wait-for-backup-minutes'])

while (path.exists(f"{backup_lockfile_path}")):
    if (wait_for_backup_minutes <= 0): error(f"Veeam wartet bereits seit {wait_for_backup_minutes} Minuten auf den Kopiervorgang, überschreite festgelegte Grenze. Abbruch")
    wait_for_backup_minutes = wait_for_backup_minutes - 1
    sleep(600)

filename = f"{datetime.now().strftime(f'%Y%m%d-%H%M%S')}.lock"
config.set(f'BACKUP', f'veeam-lockfile-path', f"{veeam_lockfile_path}{filename}")
try:
	with open(f'config.ini', 'w') as configfile:
		config.write(configfile)
	with open(f"{veeam_lockfile_path}{filename}", 'w+') as f:
		f.close
except:
	error(f"Veeam konnte kein Lockfile erstellen. Abbruch")
