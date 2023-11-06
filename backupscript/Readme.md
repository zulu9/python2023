# Backup-Copy-Script

Dieses git-repositry enthält Skripte, welche einen Kopiervorgang von Daten auf einen anderen Datenträger starten. Die Skripte enthalten neben den eigenlichen Kopiervorgang einen Mailer für Mailbenachrichtigungen und einen Webserver zum Verfolgen des Status während das Skript läuft.


## Enthaltene Files

Enthalten sind:

* asbackup.py : Hauptskript zum Starten des Kopiervorgangs sowie alle weiteren Skripte
* Backup.py : Klassendatei, enthält alle Anweisungen zum Kopiervorgang
* Mailer.py : Klassendatei, enthält alle Anweisungen für den Mailer
* webserver.py : Skript, welches den Webserver verwaltet
* config.ini.template : Enthält alle Konfigurationen, vor dem Nutzen in 'config.ini' umbenennen und ausfüllen
* veeam_lock.py : Prüft, ob ein Kopiervorgang läuft, damit nicht gleichzeitig Veeam an Backup startet. Erstellt anschließend ein Lockfile
* veeam_unlock.py : Löscht das vom Skript 'veeam_lock.py' erstellte Lockfile, wenn das Veeam-Backup fertig gestellt ist.
* rsync_excludes : File mit allen Dateien / Ordner, die beim Kopiervorgang ignoriert werden sollen
* Ordner static : Statische Resourcen für die Webseite
* Ordner templates : Templates für die Webseite 


## Verwendung

Bevor das Skript verwendet werden kann müssen einmalig ein Paar Abhängigkeiten installiert werden. Dies geschieht über 

```bash
pip install <dependency_name>
```

* flask
* waitress
* weitere tbd

Das Skript wird über das Skript 'asbackup.py' gestartet. Es werden root-Rechte benötigt. Gestartet wird es mit:

```bash
python3 asbackup.py
```


## Konfigurierung

Die 'config.ini' bietet die Möglichkeit, das Skript vielseitig zu konfigurieren. Die Werte werden als key-value Paare aufgefasst. Das Hinzufügen eigener Keys ist derzeit ineffektiv, es werden nur die bereits angegebenen Keys verarbeitet. Im Detail sind folgende Konfigurationen möglich:

**Backup**
* filesystem-ids-and-notification-mail-addresses: Eine Liste der UUIDs, auf die das Backup kopiert werden soll zusammen mit Mailadressen, die über das Ergebnis informiert werden sollen. Der erste Match mit den verfügbaren UUIDs wird verwendet. Aufzuschreiben nach dem Muster: 
```bash
UUID[,notification-mailaddress]*[,UUID[,notification-mailaddress]*]*
```
* backup-source: Quellverzeichnis, welches kopiert werden soll
* backup-destination: Zielverzeichnis, wohin die Kopie erstellt werden soll
* backup-lockfile-path: Ausgehend vom Zielverzeichnis, wo das Lockfile (verhindert weitere Zugriffe) erstellt werden soll
* veeam-lockfile-path: Wo Veeam-Lockfiles zu finden sind
* log-file-path: Speicherort des allgemeinen Logs. Kompletter Pfad + Datei
* rsync-log-file-path: Speicherort des Rsync-Logs. Kompletter Pfad + Datei
* wait-for-veeam-minutes: Wartezeit auf Veeam-Backups in Minuten
* rsync-update-ratio-seconds: Abtastrate für Rsync-Logs updates in Sekunden
* free-space-threshold-gb: Schwellwert für 'Wenig Speicherplatz'-Warnungen in GB

**Mail**
* to-mail-addresses-sysop: Zieladresse der Sysops für Mails (erhalten immer eine Mail, unabhängig der angesteckten Platte)
* from-mail-address: Sendeadresse für Mails
* cc: CC für Mails
* server: Verwendeter Mailserver
* port: Port zum verwendeten Mailserver
* username: Login-Name für den Mailserver
* password: Passwort für den Mailserver

**Webserver**
* webhost: Host für den Webserver
* webport: Port für den Webserver

**VEEAM**
* veeam-lockfiles: Ort, an denen die Veeam-Lockfiles für die Skripte 'veeam_lock.py' und 'veeam_unlock.py' zu finden sind.
* wait-for-backup-minutes: Wartezeit auf den Backup-Kopiervorgang in Minuten

**Debug**
* debug: Debugausgabe aller Umgebungsvariablen


## Fehler

Mögliche Fehler sind:

* Angegebene UUIDs stimmen nicht mit den im System verfügbaren UUIDs überein.
* Warten auf Veeam-Backup überschreitet festgelegte Höchstdauer.
* Festplatte kann nicht gemountet werden. Tritt in der Regel dann auf, wenn die Festplatte bereits gemountet ist.
* Skript gestartet, doch es wurde bereits ein Lockfile gefunden. Wahrscheinlich wurde das Skript mehrmals gestartet 
* Lockfiles können nicht erstellt werden. Schreibrechte könnten fehlerhaft sein.
* Der Kopiervorgang schlägt fehl. Weitere Infos im Rsync-Log.
* Lockfiles können nicht mehr gelöscht werden. 
* Festplatte kann nicht unmountet werden. 

## Warnungen 

Mögliche Warnungen sind:

* Ein Lockfile ist vorhanden, doch es ist leer. Wahrscheinlich war der Abschluss des letzten Backups nicht erfolgreich.
* Freier Speicherplatz ist unter dem gesetzten Schwellwert.
* Lockfiles zum löschen exitieren nicht mehr. Sie wurden wahrscheinlich anderweitig gelöscht.

## Ergebnisse / Logs

Unter den angegebenen Pfaden können die Logs eingsehen werden. Diese werden auch per Mail an die angegebenen Zieladresses als Anhang verschickt. Zudem kann, während das Skript läuft, der aktuelle Verlauf per Webserver eingesehen werden.


## Was soll das Copy-Script machen?

### Ablauf

1. Das Script wird gestartet, eine Filesystem-ID wird übergeben.
(Alternativ: Im System verfügbare Filesystem-IDs werden mit einer Liste abgeglichen)
    * Falls keine gültige ID: Abbruch

2. Das Script überprüft, ob gerade ein Veeam-Backup läuft, indem es nach Lock-Files in einem configuriertem Verzeichnis sucht.
    * Falls existiernd: Bis zu einem konfiguriertem Timeout warten. Nach dem Timeout: Abbruch

3. Das Script mounted die Festplatte - falls Fehlschlag abbruch

4. Das Script erzeugt ein Lockfile auf der Festplatte (samt unix file-lock)
    * Falls ein lockfile-file ohne file-lock existiert: Warnung schreiben und lock erzeugen (Kopiervorgang wurde unvollstöndig abgeprochen)
    * Falls ein Lockfile-file mit file-lock existiert: Abbruch (Script wurde 2x gestartet)
    * Falls aus technischen Gründen kein lock-file erstellt werden kann: Abbruch.

5. Falls auf der Festplatte zu wenig Speicherplatz vorhanden ist, Abbruch (Hinweis: rsync dry-run sollte dies feststellen können)

6. Rsync-Kopier-Prozess starten und return-code überprüfen
    * Falls != 0 (d.h. rsync-Fehler), Abbruch
    * Falls laufend: Alle x=30 Sekunden (konfigurierbar) status lesen und ein Textdatei schreiben.

7. Lock-File löschen
    * Falls nicht möglich, Abbruch

8. Freien Speicherplatz auf der externen Festplatte ermitteln
    * Falls eine bestimmten Grenze unterschritten wird: Warnung loggen.

9. Festplatte unmounten, terminieren

### Sonstige Anforderungen

1. Bei einem Abbruch sollte (soweit möglich), das lock-file gelöscht und die Festplatte unmounted werden
2. Bei Beginn und am Ende wird eine E-Mail an eine konfiguriere Adresse gesendet.
Diese E-Mail enthält das Ergebnis (d.h. Terminiert oder Abbruch), alle Warnungen und den freien Speicherplatz der Platte. Sollte das Backup erfolgreich sein sollten nicht mehr als 10 Zeilen ausgegeben werden. 
3. Jeder Schritt erzeugt mindestens eine log-Nachricht mit Level info - Abbrüche eine mit Level error in einem Textfile
4. Das lock-file wird im Quellverzeichnis erstellt. rsync kopiert keine lockfiles in das Zielverzeichnis.
5. Alle Kommandos werden mit sudo-Ausgeführt
6. Kann eine mounted Festplatte nicht unmounted, dann wird sync ausgeführt. 
7. Alle für den Betrieb notwendigen Dateien (udev-Regeln, Systemd-regel, Windows .cmd-Startet) sind Teil dieses git-Repositories.

## Was sollen die Veeam-Scripte tun

### 1. Pre-Backup

1. Wenn gestartet, überprüfe ob ein Copyscript-Lockfile existiert.
    * Falls ja, bis zu einem Timout warten, dann abbruch (8h Timeout) Abbruch (und E-Mail)

2. Ein Veam-Lockfile erstellen.
    * Falls kein Lockfile erstellt werden kann: Abbruch (und E-Mail)
    * Existierende Lockfiles können ignoriert werden.

### 2. Post-Backup
1. Wenn gestartet, ein Veeam-Lockfile löschen.


## Nicht-funktionale Anforderungen

* CONFIG = configparser.ConfigParser() verwenden
* Unix-Commandos als Python String-Interpolation, nicht konfigurierbar
* PyUnit-Tests auf String-Asserts der Shell-Commnds (d.h. Executor: Sudo / string) für Tests progammatisch konfigurierbar. - Alternativ: Mocking der Python-API. - Sinnvoll ggf. Tests für die verschiedenen Fehlerfälle.

## Nice-to-have

* Script läuft aus flask-prozess, der Kopiervorgang wird URL-aufruf (z.B. /copy) gestartet
* Das Veeam-Pre-Script und das Veeam-Post-Script kennen die ID der Job-execution und erstellt bzw. löscht das passende lockfile. Es gibt einen Aufräum-Mechanismus um lockfiles alter job-execution zu löschen. (Veeam hat eine Rest-API - Jan hat jetzt aber nur die Jobs und nicht die Ausführungen in der API-Doc gefunden :-( )
* Progress / Zeitschätzung: Rsync kann über `--dry-run` ermitteln, welche Daten kopiert werden müssen. Bevor der Kopiervorgang gestartet (bei Schritt 5) wird rsync (mit den gleichen Parameter) aber als `--dry-run` gestartet. Das Script parsed wie viele Daten kopiert werden müssen und logged auch diesen Fortschritt in Schritt 5 alle z.B. 10 Sekunden gemeinsam mit dem Progress
* CI-Integration für: Debian oder Pip-Paket, sowie windows .exe-file.


# Offene ToDos (Meeting 28.10)

## Dokumentation

- Readme, doch noch keine genaue Beschreibung wie das Skript zu starten ist
- ALambertz: Readme ergänzen, was ist im Repo enthalten, wie wird es verwendet, configs, welche Fehler gibt es, was wird gelogt, ... 28.10.
- Thomas/Zeineb: Wie wird das Skript in udev eingehangen, Hinweise zur Nutzung des Skriptes
- Deployment/Installationsanleitung (git-repo clonen, python dependencies, ...)


## offene Implementierungen (ALambertz, 28.10)

- Progress-Report über Web (Hinweis bzgl. des Reports: Kann auch wesentlich schneller fertig werden, da ..)
- Check auf Veeam Backups 
- Check einbauen, ob Atlantis Zugriff auf die Veeam-Backups hat
- Wording der Logs (Verständlich auch für nicht-entwickler und Konsequenzen aus Fehlern)
- Lockfile locken
- Veeam-Helferskripte
    - prüft noch nicht, ob das backup-skript auf Atlantis läuft
    - Review, ob alle Anforderungen angegangen worden sind
- Für Debugs: Dumping aller Umgebungsvariablen
- Rsync soll in ein eigenes Log schreiben


## Testen

- Email-Benachrichtung (Thomas, in Abstimmung mit Zeineb/Sibylle)
    - Wording anpassen
    - Log immer versenden
- Wording für den Progress-Report/Log übers Web (Thomas, in Abstimmung mit Zeineb/Sibylle)
- Funktionstests (Thomas, 31.10)
- Falls alles funktioniert: Test auf Atlantis (Thomas/Zeineb, 31.10)
