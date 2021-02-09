#!/usr/bin/env python3

from email import message_from_bytes
from configparser import ConfigParser
from imapclient import IMAPClient
from notifypy import Notify
from keyring import get_password, set_password
from argparse import ArgumentParser
from getpass import getpass
from appdirs import user_config_dir
from os import path

def main():
    app_name = "emailnotify"
    author = "kanashimia"

    args_parser = ArgumentParser()
    args_parser.add_argument('-p', action='store_true', dest='password',
        help='prompts for a password, and stores it in the credential store')
    args_parser.add_argument('-c', dest='config',
        help='set config file location')
    args = args_parser.parse_args()

    config_path = args.config or path.join(user_config_dir(app_name, author), "config.ini")

    if not path.exists(config_path):
        exit(f"Error: no config found in {config_path}")

    config_parser = ConfigParser()
    config_parser.read(config_path)

    mail = config_parser["mail"]

    if(args.password):
        set_password(app_name, mail["username"], getpass())

    password = get_password(app_name, mail["username"])
    if not password:
        exit(f"Error: password is empty, please add it by running '{app_name} -p'")

    folder = mail.get("folder","INBOX")

    server = IMAPClient(mail["host"])
    server.login(mail["username"], password)
    server.select_folder(folder, readonly=True)

    notif = Notify()

    while True:
        try:
            next_uid = server.folder_status(folder)[b"UIDNEXT"]

            server.idle()
            responses = server.idle_check()
            server.idle_done()

            results = server.fetch(next_uid, b"ENVELOPE")

            for result in results.values():
                envelope = result[b"ENVELOPE"]
                notif.title = "New email!"
                notif.message = envelope.subject.decode()
                notif.send(block=False)

        except KeyboardInterrupt:
            server.idle_done()
            server.logout()
            break
