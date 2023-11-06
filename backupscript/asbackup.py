#!/usr/bin/python3
import traceback
import configparser
import datetime
from Backup import Backup
from Mailer import Mailer
from webserver import app
from waitress import serve
from threading import Thread
from os import environ
from time import sleep

def do_backup(backup: Backup, mailer: Mailer):
    try: 
        try:
            backup.checkFilesystem()
            backup.checkVeeamBackup()
            backup.mountHDD()
        except Exception:
            raise Exception

        try:
            backup.createLockfile()
        except Exception:
            try: 
                backup.unmountHDD()
            except Exception:
                pass
            raise Exception
            
        try:
            backup.startCopy()
            backup.calcFreeSpace()
            mailer.addSubject(0, "")
        except Exception:
            pass
        finally:
            try: 
                backup.deleteLockfile()
                backup.unmountHDD()
            except:
                raise Exception
    except Exception:
        mailer.addException(traceback.format_exc())
    finally:
        mailer.addText(f"Backup beendet am {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        mailer.sendMail()

def runWebserver():
    try:
        serve(app, host=config['WEBSERVER']['webhost'], port=config['WEBSERVER']['webport'])
    except:
        print(f"ERROR: Webserver konnte nicht auf Port \"{config['WEBSERVER']['webhost']}:{config['WEBSERVER']['webport']}\" gestartet werden.")

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("config.ini")

    if (config['DEBUG']['debug'] == 'true') : 
        for k, v in sorted(environ.items()):
            print(k+':', v)
        print('\n')
        [print(item) for item in environ['PATH'].split(';')]

    try:
        server_thread=Thread(target=runWebserver, daemon=True)
        server_thread.start()
    except:
        print(traceback.format_exc())

    mailer: Mailer = Mailer()
    backup: Backup = Backup(mailer, "prod")
    do_backup(backup, mailer)
    sleep(3600) # Webserver active for 1h after Script finishes
