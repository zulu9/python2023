#!/usr/bin/python3
import os
import configparser

config = configparser.ConfigParser()
config.read(f"config.ini")

path = config['VEEAM']['veeam-lockfiles']
file = config['BACKUP']['veeam-lockfile-path']
if os.path.exists(path) and not os.path.isfile(path):
    # Checking if the directory is empty or not
    if not os.listdir(path):
        print (f"Empty directory")
    else:
        try:
            print (f"Try removing {file}")
            os.remove(file)
            print(f"Veeam-Lockfile successfully removed")
        except:
            print(f"Could not remove file {file}. Already removed?")
else:
        print ("Could not open directory")
