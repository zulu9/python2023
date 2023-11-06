#!/usr/bin/python3
import subprocess, sys, os
import argparse
import logging
import logging.handlers
from sh import mount,umount
from shutil import disk_usage
from flask import Flask, render_template
from waitress import serve
import time
from time import sleep
from threading import Thread
import smtplib
from email.message import EmailMessage

script_path=(os.path.abspath(os.path.dirname(__file__)))

#CONFIGURATION
#Parse command line arguments
#-----------------------------
parser = argparse.ArgumentParser("asbackup.py")
parser.add_argument("uuid", help="UUID of the external HDD e.g. \"33cb9790-30b8-42e6-bdb5-86bb73fafffc\"")
parser.add_argument("dest", help="Mountpoint for the external HDD, e.g. \"/media/extBackupBackoffice/\"")
parser.add_argument('--fstype', help="File system of the external HDD.", nargs='?', default="ntfs-3g")
parser.add_argument('--email', help="Send email notification to sysop and this recipient, e.g. backoffice@anderscore.com", nargs='?', default=False)
parser.add_argument('--src', help="Source mountpoint of the Backup, defaults to /media/veeambackupshare/", nargs='?', default="/media/veeambackupshare/")
parser.add_argument('--log', help="Location of the log files, defaults to /srv/scripts/as-backupscript/logs/asbackup.log", nargs='?', default="/srv/scripts/as-backupscript/asbackup.log")
parser.add_argument('--loglevel', help="Loglevel. Can be debug, info, warning or error. Defaults to info.",nargs='?', default="info")
args = parser.parse_args()

#--------------------------------------------------------------------------------------------------------------------------------
#Configure loggers
#-----------------------------
#Set log format and level
log_format = logging.Formatter("%(asctime)s [%(threadName)s]  %(message)s")
my_logger = logging.getLogger()

loglevel=str(args.loglevel)
if loglevel=="debug":
    my_logger.setLevel(logging.DEBUG)
elif loglevel=="warning":
    my_logger.setLevel(logging.WARNING)
elif loglevel=="error":
    my_logger.setLevel(logging.ERROR)
else:
    my_logger.setLevel(logging.INFO)

#Log to file
logfile=str(args.log)
file_handler =  logging.handlers.RotatingFileHandler(logfile, mode = 'w', backupCount = 10)
file_handler.setFormatter(log_format)
my_logger.addHandler(file_handler)

#Also log to console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
my_logger.addHandler(console_handler)

my_logger.info("LOGLEVEL: "+loglevel)

#Rsync-Logfile
current_date=time.strftime("%Y%m%d")
rsync_logfile=script_path+'/rsync-'+current_date+'.log'

#Initialize checks as False/not yet done
#-----------------------------
#Prep checks
veeamlock_check=False
mount_check=False
lockfile_check=False
veeam_backup_check=False
freespace_before_check=False

#Post checks
freespace_after_check=False
unlockfile_check=False
umount_check=False

#1=Erfolgreich abgeschlossen
#2=Noch nicht entschieden
#3=Nicht erfolgreich abgeschlossen
prep_checks_passed=2
post_checks_passed=2
rsync_check_passed=2

#Configure paths, devicenames etc.
#-----------------------------
#Pfad zu den Veeam Backups
veeam_backup_path=str(args.src)
#Veeam Lockfile: Verzeichnis mit veeam-Lockfiles. Muss ein leeres sein.
veeamlock_path=veeam_backup_path+"veeamlocks"
#Veeam Checkfile: Muss vorhanden sein und die erste Zeile muss "veeam" lauten.
veeam_checkfile_path=veeam_backup_path+"veeamcheck.txt"

mount_uuid="-U"+str(args.uuid)
mount_dest=str(args.dest)
mount_options="-t"+str(args.fstype)
#Lockfile: Darf bei Start des Scripts nicht vorhanden sein. Wird während des Scripts erstellt (Inhalt "locked") und am Ende entfernt.
lockfile_path=mount_dest+"backup.lock"

#Webserver
webhost="0.0.0.0"
webport=8080

#Configure E-Mail notifications
#-----------------------------
from_mail_address="asbackup@anderscore.com"
sysop_mail_address="sysop@anderscore.com"

server="smtp.ionos.de"
port="587"
username="asbackup@anderscore.com"
password="!VeiQu5Thahci!"
use_tls=True
if args.email:
    notify_mail_address=str(args.email)
    notify=True
else:
    notify=False
#--------------------------------------------------------------------------------------------------------------------------------



#PREPERATION TASKS
#--------------------------------------------------------------------------------------------------------------------------------
my_logger.info ("Starting preperation tasks")
#Send start email (optional)
#-----------------------------
if notify==True:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content("Backup auf "+str(args.dest)+" gestartet. Der Status kann auf http://atlantis.ads.anderscore.com:8080/ verfolgt werden.")

    msg['Subject'] = "[backup] [start] Backup auf "+str(args.dest)+" gestartet"
    msg['From'] = from_mail_address
    msg['To'] = notify_mail_address
    msg['CC'] = sysop_mail_address

    try:
        smtp = smtplib.SMTP(server, port)
        if use_tls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)
        smtp.quit()
        my_logger.info ("SUCCESS: Start Mail sent")
    except:
        my_logger.warning ("ERROR: Something went wrong sending the start mail")
else:
    my_logger.info ("SUCCESS: No Start Mail requested.")


#Check for Veeam lockfile
#-----------------------------
# Function to Check if the path specified
# specified is a valid directory

if os.path.exists(veeamlock_path) and not os.path.isfile(veeamlock_path):
    # Checking if the directory is empty or not
    if not os.listdir(veeamlock_path):
        veeamlock_check=True
        veeamlock_message="SUCCESS: Keine Veeam Lockfiles in \""+veeamlock_path+"\" gefunden."
        my_logger.info (veeamlock_message)
    else:
        veeamlock_check=False
        veeamlock_message="ERROR: Mindestens ein Veeam Lockfile in \""+veeamlock_path+"\" gefunden."
        my_logger.error (veeamlock_message)
else:
        veeamlock_check=False
        veeamlock_message="ERROR: Konnte Veeam Lockfile Verzeichnis \""+veeamlock_path+"\" nicht öffnen."
        my_logger.error (veeamlock_message)

#Mount external HDD
#-----------------------------
if veeamlock_check==True:
    try:
        mounted=mount(mount_uuid, mount_dest, mount_options)
        mount_check=True
        mounts_message="SUCCESS: HDD mit UUID \""+str(args.uuid)+"\" unter \""+mount_dest+"\" gemountet."
        my_logger.info (mounts_message)
    except:
        mount_check=False
        mounts_message="ERROR: HDD mit UUID \""+str(args.uuid)+"\" konnte nicht unter \""+mount_dest+"\" gemountet werden."
        my_logger.error (mounts_message)
else:
        mount_check=False
        mounts_message="ERROR: Veeam lockfile gefunden. Externe HDD wird nicht gemountet."
        my_logger.error (mounts_message)

#Create Lockfile
#-----------------------------
if mount_check==True:
    try:
        with open(lockfile_path, 'r') as f:
            lock = f.readline().strip().split()
            if lock[0] == 'locked':
                lockfile_check=False
                lockfile_message="ERROR: Lockfile \""+lockfile_path+"\" existiert bereits."
                my_logger.error (lockfile_message)
                f.close
            else:
                lockfile_check=False
                lockfile_message="ERROR: Lockfile \""+lockfile_path+"\" ist korrupt."
                my_logger.error (lockfile_message)
    except FileNotFoundError:
        try:
            with open(lockfile_path, 'w') as f:
                f.write('locked')
                lockfile_check=True
                lockfile_message="SUCCESS: Lockfile \""+lockfile_path+"\" erfolgreich angelegt."
                my_logger.info (lockfile_message)
                f.close
        except:
            lockfile_check=False
            lockfile_message="ERROR: Lockfile \""+lockfile_path+"\" konnte nicht geschrieben werden."
            my_logger.error (lockfile_message)
else:
    lockfile_check==False
    lockfile_message="ERROR: Lockfile \""+lockfile_path+"\" konnte nicht angelegt werden. HDD ist nicht gemountet."
    my_logger.error (lockfile_message)


#Check if we have a valid backup to avoid overwriting with empty directory
#-----------------------------
disk_usage = disk_usage(veeam_backup_path)
used = disk_usage.used // 1024 // 1024 // 1024
try:
    with open(veeam_checkfile_path, 'r') as f:
        text = f.readline().strip().split()
        if text[0] == 'veeam':
            f.close
            veeam_backup_check=True
            veeam_backup_message="SUCCESS: \""+veeam_checkfile_path+"\" gefunden. Benutzter Speicherplatz auf \""+veeam_backup_path+"\": "+str(used)+" GB."
            my_logger.info (veeam_backup_message)
        else:
            f.close
            veeam_backup_check=False
            veeam_backup_message="ERROR: \""+veeam_checkfile_path+"\" ist korrupt. Benutzter Speicherplatz auf \""+veeam_backup_path+"\": "+str(used)+" GB."
            my_logger.error (veeam_backup_message)
except FileNotFoundError:
    veeam_backup_check=False
    veeam_backup_message="ERROR: \""+veeam_checkfile_path+"\" nicht gefunden. Kann nicht auf Veeam-Backups zugreifen."
    my_logger.error (veeam_backup_message)

#Combine prep checks and make list for Flask App
#-----------------------------
if veeamlock_check==True and mount_check==True and lockfile_check==True and veeam_backup_check==True:
    prep_checks_passed=1
    my_logger.info ("SUCCESS: All preperation checks PASSED")
else:
    prep_checks_passed=3
    my_logger.error ("ERROR: At least one preperation check failed.")
prep_messages_list=[mounts_message, lockfile_message, veeamlock_message,veeam_backup_message]

#Initial messages for post-copy tasks (will be filled later by post_copy_tasks function)
#-----------------------------
unlockfile_message="Lockfile: Noch nicht fertig."
umount_message="Umount: Noch nicht fertig."
post_messages_list=[unlockfile_message, umount_message]
my_logger.info ("Preperation tasks DONE")
#--------------------------------------------------------------------------------------------------------------------------------



#POST COPY TASKS
#--------------------------------------------------------------------------------------------------------------------------------
#Do things after rsync finished or failed
#-----------------------------
def post_copy_tasks():
    #Make messages available outside function
    #-----------------------------
    global post_checks_passed
    global post_messages_list
    #Remove lockfile
    #-----------------------------
    if lockfile_check==True:
        try:
            os.remove(lockfile_path)
            unlockfile_check=True
            unlockfile_message="SUCCESS: Lockfile \""+lockfile_path+"\" erfolgreich entfernt."
            my_logger.info (unlockfile_message)
        except:
            unlockfile_check=False
            unlockfile_message="ERROR: Lockfile \""+lockfile_path+"\" konnte nicht entfernt werden."
            my_logger.error (unlockfile_message)
    else:
        unlockfile_check=False
        unlockfile_message="ERROR: Lockfile wurde durch einen vorherigen Fehler nicht angelegt oder existierte bereits."
        my_logger.error (unlockfile_message)

    #Unmount the external HDD
    #-----------------------------
    if mount_check==True:
        try:
            umount (mount_dest)
            umount_message="SUCCESS: Umount von \""+mount_dest+"\" erfolgreich."
            umount_check=True
            my_logger.info (umount_message)
        except:
            umount_message="ERROR: Umount fehlgeschlagen."
            umount_check=False
            my_logger.error (umount_message)
    else:
        umount_check=False
        umount_message="ERROR: Mount fehlgeschlagen. Umount nicht nötig."
        my_logger.error (umount_message)

    #Combine post checks and make list for Flask app
    #-----------------------------
    if unlockfile_check==True and umount_check==True:
        post_checks_passed=1
        my_logger.info ("All post checks PASSED")
    else:
        post_checks_passed=3
        my_logger.error ("ERROR: At least one post check failed")
    post_messages_list=[unlockfile_message, umount_message]

    #Send end Email (optional)
    #-----------------------------
    if notify==True:
        if prep_checks_passed==1 and rsync_check_passed==1 and post_checks_passed==1:
            mail_subject="[backup] [finish] Backup auf "+str(args.dest)+" erfolgreich beendet."
        else:
            mail_subject="[backup] [error] Backup auf "+str(args.dest)+" fehlgeschlagen."

        # Open the current logfile to send as Email content
        with open(logfile,'r') as fp:
            # Create a text/plain message
            msg = EmailMessage()
            msg.set_content(fp.read())
        msg['Subject'] = mail_subject
        msg['From'] = from_mail_address
        msg['To'] = notify_mail_address
        msg['CC'] = sysop_mail_address

        try:
            smtp = smtplib.SMTP(server, port)
            if use_tls:
                smtp.starttls()
            smtp.login(username, password)
            smtp.send_message(msg)
            smtp.quit()
            my_logger.info ("SUCCESS: End mail sent")
        except:
            my_logger.warning ("ERROR: Something went wrong sending the end mail")
    else:
        my_logger.info ("SUCCESS: No end mail requested.")
#--------------------------------------------------------------------------------------------------------------------------------


#RUN RSYNC
#--------------------------------------------------------------------------------------------------------------------------------
# Function to check if rsync is still running and call post_copy_tasks afterwards
#-----------------------------
def run_tasks():
    global rsync_check_passed
    global rsync_status
    #Check if rsync is still running
    if prep_checks_passed==1:
        while rsync_process.poll() is None:
            my_logger.debug ("Rsync still running...")
            rsync_check_passed=2
            retcode=None
            try:
                rsync_status="Status: "+rsync_process.stdout.readlines()[-1]
            except:
                rsync_status="Rsync-Status unbekannt. Bitte laden Sie die Seite erneut (F5)."
            my_logger.debug (rsync_status)
            #Check interval
            sleep(2)

        #Rsync is done. Get return code and Rsync's log
        retcode=rsync_process.poll()
        with open(rsync_logfile,'r') as file:
            rsync_log = file.read()
        #os.remove(rsync_logfile)

        #Rsync finished successfully
        if retcode==0:
            rsync_check_passed=1
            rsync_status="SUCCESS: Kopiervorgang erfolgreich abgeschlossen."
            my_logger.info (rsync_status+" Return Code:"+str(retcode))
            my_logger.info ("\n---RSYNC LOG START---\n"+rsync_log+"---RSYNC LOG END---\n")
        #Rsync had an error
        else:
            rsync_check_passed=3
            rsync_status="ERROR: Kopiervorgang mit Fehler abgebrochen. Return code: "+str(retcode)
            my_logger.error (rsync_status)
            my_logger.error ("\n---RSYNC LOG START---\n"+rsync_log+"---RSYNC LOG END---\n")
    else:
        rsync_check_passed=3

    #Start post-copy tasks
    my_logger.info ("Starting post-copy tasks")
    post_copy_tasks()
    my_logger.info ("Post-Copy tasks DONE")
    #Keep Webserver alive for some time after everything is done
    sleep (60)
    #input ("Press Enter to quit")
    #Save logfile
    logging.handlers.RotatingFileHandler.doRollover(file_handler)

#------------------------------------------------------------------------
#If all checks passed start rsync and post-copy tasks and display status
#------------------------------------------------------------------------
if prep_checks_passed==1:
    #Start Rsync
    #-----------------------------
    #Commands to run
    #Test commands
    #cmd= [script_path+'/dummy.sh']
    #cmd = ['wget', 'https://speed.hetzner.de/10GB.bin','-O10GB.bin']
    #cmd=['ping','-c 10','google.de']

    #Actual rsync command
    cmd=['rsync','-rvht','--size-only','--log-file='+rsync_logfile,'--exclude-from='+script_path+'/rsync_excludes','--info=progress2','--inplace','--delete-before',veeam_backup_path,mount_dest]

    # Start running rsync as subprocess and set it to non-blocking
    try:
        rsync_process=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,text=True)
        os.set_blocking(rsync_process.stdout.fileno(), False)
        rsync_status="SUCCESS: Kopiervorgang gestartet."
        my_logger.info(rsync_status)
    except:
        rsync_check_passed=3
        rsync_status="ERROR: Start von Rsync fehlgeschlagen. Kopiervorgang wurde nicht gestartet."
        my_logger.error(rsync_status)
else:
    rsync_status="ERROR: Vorbereitungen fehlgeschlagen. Kopiervorgang wurde nicht gestartet."
    my_logger.error(rsync_status)
    prep_checks_passed=3
    rsync_check_passed=3
# create a thread for the run_tasks function
tasks_thread=Thread(target=run_tasks)
# run the thread
tasks_thread.start()
#--------------------------------------------------------------------------------------------------------------------------------


#WEB VIEW
#--------------------------------------------------------------------------------------------------------------------------------
#Initiate Flask App
#-----------------------------
app=Flask('aSBackup',template_folder=script_path+'/templates',static_folder=script_path+'/static')
@app.route('/')
def index():
    return render_template('index.html', prep_messages=prep_messages_list, post_messages=post_messages_list, prep_checks_passed=prep_checks_passed, post_checks_passed=post_checks_passed, rsync_check_passed=rsync_check_passed, rsync_status=rsync_status)

#Run Flask App as deamon
#-----------------------------
if __name__ == '__main__':
    #Create a thread for the waitress web-server and start it
    def run_server():
        try:
            serve(app, host=webhost, port=webport)
        except:
            my_logger.error("ERROR: Webserver konnte nicht auf Port \""+str(webhost)+":"+str(webport)+"\" gestartet werden.")
    try:
        server_thread=Thread(target=run_server,daemon=True)
        server_thread.start()
    except:
        my_logger.error("ERROR: Webserver konnte nicht auf Port \""+str(webhost)+":"+str(webport)+"\" gestartet werden.")
#--------------------------------------------------------------------------------------------------------------------------------
