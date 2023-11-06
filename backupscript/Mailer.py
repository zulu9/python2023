import configparser
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Mailer:

    def __init__(this):
        this.config = configparser.ConfigParser()
        this.config.read("config.ini")
        this.backup_source = this.config['BACKUP']['backup-source']
        this.log_file_path = this.config['BACKUP']['log-file-path']
        this.rsync_log_file_path = this.config['BACKUP']['rsync-log-file-path']
        this.from_mail_address = this.config['MAIL']['from-mail-address']
        this.to_mail_addresses = this.config['MAIL']['to-mail-addresses-sysop'].replace(" ", "").split(",")
        this.mail_cc = this.config['MAIL']['cc']
        this.server = this.config['MAIL']['server']
        this.port = this.config['MAIL']['port']
        this.username = this.config['MAIL']['username']
        this.password = this.config['MAIL']['password']
        this.mail_text = this.mail_warnings = this.mail_errors = this.mail_exceptions = this.mail_body = ""

        this.msg = MIMEMultipart()
        this.msg['From'] = this.from_mail_address
        this.msg['CC'] = this.mail_cc

    def addRecipents(this, recipents: str):
        if (recipents != ""): 
            for recipent in recipents.split(","): this.to_mail_addresses.append(recipent)

    def addSubject(this, status: int, text: str):
        if (this.msg['Subject'] is None):
            if (status == 0):
                this.msg['Subject'] = f"[backup] [success] Backup erfolgreich"
            elif (status == 1):
                this.msg['Subject'] = f"[backup] [failed] {text}"
            elif (status == 2):
                this.msg['Subject'] = f"[backup] [start] {text}"
            else:
                this.msg['Subject'] = f"[backup] [failed] Skript wurde unerwartet abgebrochen"

    def addText(this, text):
        this.mail_text += f"{text}\n"

    def addWarning(this, warning):
        this.mail_warnings += f" - {warning}\n"

    def addError(this, error):
        this.mail_errors += f" - {error}\n"

    def addException(this, exception):
        this.mail_exceptions += f"{exception}\n"

    def sendMail(this):
        if (this.mail_text != ""): this.msg.attach(MIMEText(f"{this.mail_text}", "plain"))
        if (this.mail_errors != ""): this.msg.attach(MIMEText(f"[ERRORS]\n{this.mail_errors}", "plain"))
        if (this.mail_warnings != ""): this.msg.attach(MIMEText(f"[WARNINGS]\n{this.mail_warnings}", "plain"))
        if (this.mail_exceptions != ""): this.msg.attach(MIMEText(f"[TRACEBACK]\n{this.mail_exceptions}", "plain"))
        
        if (not str(this.msg['Subject']).startswith(f"[backup] [start]")): 
            try:
                with open(f"{this.log_file_path}",'r') as attachment:
                    part = MIMEBase("text", "plain")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {this.log_file_path.split('/')[-1]}")
                this.msg.attach(part)
            except: pass
            try:
                with open(f"{this.rsync_log_file_path}",'r') as attachment:
                    part = MIMEBase("text", "plain")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {this.rsync_log_file_path.split('/')[-1]}")
                this.msg.attach(part)
            except: pass

        try:
            smtp = smtplib.SMTP(this.server, this.port)
            smtp.starttls()
            smtp.login(this.username, this.password)
            for to_mail_address in this.to_mail_addresses:
                this.msg['To'] = to_mail_address
                print(this.msg['Subject'])
                if 'Subject' not in this.msg : this.msg['Subject'] = f"[backup] [failed] Skript wurde unerwartet abgebrochen"
                smtp.send_message(this.msg)
                del this.msg['To']
        except:
            if (str(this.msg['Subject']).startswith(f"[backup] [start]")): print("Login auf den Mailserver fehlgeschlagen. Falsche Nutzerdaten?")
        finally:
            smtp.quit()
            del this.msg['Subject']
            this.msg.set_payload([])

        this.mail_text = this.mail_info = this.mail_warnings = this.mail_errors = this.mail_exceptions = ""

if __name__ == '__main__':
    print(f"This script does nothing on its own. Please use 'asbackup.py' to start the backup.")
