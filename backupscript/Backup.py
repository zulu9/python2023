import configparser
import subprocess
import logging
import datetime
import warnings
from Mailer import Mailer
from webserver import showOnWebserver
from os import path, remove, set_blocking, listdir
from time import sleep
from shutil import disk_usage

class Backup:

    def __init__(this, mailer: Mailer, scope) -> None:
        this.config = configparser.ConfigParser()
        this.config.read("config.ini")
        this.scope = scope

        this.uuids_mailaddresses_list = this.config['BACKUP']['filesystem-ids-and-notification-mail-addresses'].replace(" ", "").split(",")
        this.uuids_mailaddresses_map = {}; mailaddresses = ""
        for item in this.uuids_mailaddresses_list[::-1]:
            if (item.find(f"@") == -1): 
                if mailaddresses.startswith(f","):
                    mailaddresses = mailaddresses[1:]
                this.uuids_mailaddresses_map[item] = mailaddresses
                mailaddresses = ""
            else: mailaddresses = f"{mailaddresses},{item}"

        this.backup_source = this.config['BACKUP']['backup-source']
        this.backup_destination = this.config['BACKUP']['backup-destination']
        this.veeam_lockfile_dir = this.config['BACKUP']['veeam-lockfile-dir']
        this.log_file_path = this.config['BACKUP']['log-file-path']
        this.rsync_log_file_path = this.config['BACKUP']['rsync-log-file-path']
        this.wait_for_veeam_minutes = int(this.config['BACKUP']['wait-for-veeam-minutes'])
        this.backup_lockfile_path = f"{this.backup_destination}/{this.config['BACKUP']['backup-lockfile-path']}"
        this.rsync_update_ratio_seconds = int(this.config['BACKUP']['rsync-update-ratio-seconds'])
        this.free_space_threshold_gb = int(this.config['BACKUP']['free-space-threshold-gb'])

        if path.exists(f"{this.log_file_path}"): remove(f"{this.log_file_path}")
        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=f"{this.log_file_path}", format='%(asctime)s  [%(levelname)-7s]  -  %(message)s', level=logging.INFO)

        if (mailer is not None): this.mailer = mailer

    def checkFilesystem(this) -> int:
        available_uuids = subprocess.getoutput("sudo blkid -s UUID -o value").split("\n")
        for uuid_to_mount in this.uuids_mailaddresses_map.keys():
            for available_uuid in available_uuids:
                if (uuid_to_mount == available_uuid):
                    this.uuid = uuid_to_mount
                    if (hasattr(this, "mailer")): 
                        this.mailer.addRecipents(this.uuids_mailaddresses_map.get(this.uuid))
                        this.mailer.addSubject(2, f"Backup gestartet auf {this.backup_destination} mit UUID {this.uuid}")
                        this.mailer.addText(f"Backup gestartet am {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} auf {this.backup_destination} mit UUID {this.uuid}. Verfolgung möglich über http://atlantis.ads.anderscore.com:8080/ .")
                        this.mailer.sendMail()
                    this.ok(f"Festplatte mit der UUID {this.uuid} lokalisiert", f"prep", f"Datenträger lokalisieren")
                    return this.uuid
        this.error(f"Festplatten der angegebenen UUID konnten nicht gefunden werden. Abbruch. Verfügbare UUIDs: \n\t{available_uuids}", f"prep", f"Datenträger lokalisieren")

    def checkVeeamBackup(this) -> int:
        while listdir(f"{this.veeam_lockfile_dir}"):
            if (this.wait_for_veeam_minutes <= 0): this.error(f"Veeam erstellt bereits seit {this.wait_for_veeam_minutes} Minuten ein Backup, überschreite festgelegte Grenze. Abbruch", f"prep", f"Warte auf Veeam-Backup")
            this.wait_for_veeam_minutes = this.wait_for_veeam_minutes - 1
            logging.info(f"Veeam erstellt weiterhin ein Backup...")
            sleep(60)
        this.ok(f"Veeam führt gerade kein Backup durch. Setze Kopiervorgang fort.", f"prep", f"Warte auf Veeam-Backup")
        return 0

    def mountHDD(this) -> int:
        if (not path.exists(f"{this.backup_destination}")): subprocess.run(f"sudo mkdir {this.backup_destination}", shell=True)
        out = subprocess.getoutput(f"sudo mount -o noatime UUID={this.uuid} {this.backup_destination}")
        if (out != ""): this.error(f"Festplatte mit der UUID {this.uuid} konnte nicht eingehangen werden. Fehlermeldung: {out}", f"prep", f"Datenträger mounten")
        this.ok(f"Festplatte mit der UUID {this.uuid} wurde erfolgreich eingehangen.", f"prep", f"Datenträger mounten")
        return 0
        
    def createLockfile(this) -> int:
        try:
            if (path.exists(f"{this.backup_lockfile_path}")):
                with open(f"{this.backup_lockfile_path}", 'r') as f:
                    if (f.readline().find("locked") != -1): 
                        this.error(f"Lockfile mit Inhalt gefunden. Wurde das Skript doppelt gestartet? Abbruch", f"prep", f"Lockfile erstellen")
                this.warn(f"Lockfile ohne Inhalt gefunden. Letzter Kopiervorgang eventuell nicht korrekt terminiert.", f"prep", f"Lockfile erstellen")
            with open(f"{this.backup_lockfile_path}", "w") as f:
                f.write("locked")
            this.ok(f"Lockfile erstellt", f"prep", f"Lockfile erstellen")
            return 0
        except: this.error(f"Lockfile konnte nicht erstellt werden. Abbruch", f"prep", f"Lockfile erstellen")

    def startCopy(this) -> int:
        logging.info(f"Kopiervorgang wird gestartet")
        rsync = subprocess.Popen(f"sudo rsync -hrtv --size-only --delete-before --log-file={this.rsync_log_file_path} --stats --info=progress2 --inplace --exclude-from=rsync_excludes {this.backup_source} {this.backup_destination}", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
        set_blocking(rsync.stdout.fileno(), False)
        while rsync.poll() is None:
            sleep(this.rsync_update_ratio_seconds)
            try:
                update = rsync.stdout.readlines()[-1]
                if (this.scope == "prod"):
                    logging.info(update)
                    this.sendToWebserver(f"rsync", f"{update}", 0)
            except:
                continue
        if (rsync.poll()): this.error(f"Kopiervorgang fehlerhaft. Abbruch")
        return 0

    def calcFreeSpace(this) -> int:
        free_space = disk_usage(this.backup_destination).free // 1024 // 1024 // 1024
        if (free_space < this.free_space_threshold_gb): this.warn(f"Freier Speicherplatz auf der Festplatte gering: {free_space}GB. Weitere Backups könnten nicht mehr möglich sein.", f"post", f"Freien Speicher berechnen")
        else: this.mailer.addText(f"Verfügbarer freier Speicherplatz: {free_space}\n")
        return 0

    def deleteLockfile(this) -> int:
        try:
            if (path.exists(f"{this.backup_lockfile_path}")):
                remove(f"{this.backup_lockfile_path}")
                this.ok(f"Lockfile gelöscht", f"post", f"Lockfile löschen")
            else: 
                this.warn(f"Lockfile existiert nicht mehr. Wurde es manuell gelöscht?", f"post", f"Lockfile löschen")
                return 1
        except: this.error(f"Lockfile konnte nicht gelöscht werden. Abbruch", f"post", f"Lockfile löschen")
        return 0

    def unmountHDD(this) -> int:
        subprocess.run(f"sudo sync", shell=True)
        out = subprocess.getoutput(f"sudo umount {this.backup_destination}")
        if (out == ""): logging.info(f"Festplatte mit der UUID {this.uuid} konnte erfolgreich ausgehangen werden.")
        else: logging.error(f"Festplatte konnte nicht ausgehangen werden. Fehlermeldung: {out}", f"post", f"Datenträger unmounten")
        return 0

    def ok(this, message, step, action) -> None:
        if (this.scope == "prod"):
            logging.info(message)
            this.sendToWebserver(step, action, 0)

    def warn(this, warning, step, action) -> None:
        if (this.scope == "prod"):
            logging.warning(warning)
            this.sendToWebserver(step, action, 1)
            if (hasattr(this, "mailer")): this.mailer.addWarning(warning)
        elif (this.scope == "test"): warnings.warn(warning)

    def error(this, error, step, action) -> None:
        if (this.scope == "prod"):
            logging.error(error)
            this.sendToWebserver(step, action, 2)
            if (hasattr(this, "mailer")): 
                this.mailer.addSubject(1, f"Backup fehlgeschlagen on {this.backup_destination}")
                this.mailer.addError(error)
        raise ValueError(error)

    def sendToWebserver(this, step, action, status) -> None:
        message = {}; message['step'] = step; message['action'] = f"{action:<30s}"; message['status'] = status; 
        showOnWebserver(message)

if __name__ == '__main__':
    print(f"This script does nothing on its own. Please use 'asbackup.py' to start the backup.")
