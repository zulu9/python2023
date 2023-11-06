from flask import Flask, render_template
from os import path

prep_messages = []
rsync_messages = ["Kopiervorgang noch nicht gestartet."]
post_messages = []

script_path = (path.abspath(path.dirname(__file__)))
app = Flask('aSBackup', template_folder = script_path+'/templates', static_folder = script_path+'/static')

@app.route('/')
def index():
    return render_template('index.html', 
                            prep_messages=prep_messages, 
                            rsync_messages=rsync_messages[-1], 
                            post_messages=post_messages)

def showOnWebserver(message) -> None:
        if message['step'] == 'prep': prep_messages.append(message)
        elif message['step'] == 'rsync': rsync_messages.append(message)
        elif message['step'] == 'post': post_messages.append(message)
        else: error(f"[WEBSERVER] Bei der Verarbeitung der Statusmeldungen ist ein Fehler aufgetreten. 'Step' war '{message['step']}', erwartet sind 'prep', 'rsync', oder 'post'.")

def error(error) -> None:
    raise ValueError(error)

if __name__ == '__main__':
    print(f"This script does nothing on its own. Please use 'asbackup.py' to start the backup.")