#!/usr/bin/python3
#-*- coding: utf-8 -*-

import smtplib
import mimetypes
import os, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Import default vars
from myutil import defaults
defaults = defaults.mail

home = os.path.expanduser("~")
user_settings_file = os.path.join(home, "myutil_settings.json")

defaults = dict(defaults)

if os.path.exists(user_settings_file):
    with open(user_settings_file) as file:
        user_defaults = json.load(file)["mail"]
    defaults.update(user_defaults)

class Mail:
    def __init__(self, sender=None, server=None, port=None, sendfile=None, filepath=None, password=None):
        """ Sort out the given variables and if neccessary fill in default variables
            or give all parameters:
            from myutil import Mail
            instance = Mail(sender, mailserver, port, true, "/path/to/file", password)
        """

        self.server = server if server is not None else defaults["server"]
        self.port = port if port is not None else defaults["port"]
        self.sendfile = sendfile if sendfile is not None else defaults["sendfile"]
        self.filepath = filepath if filepath is not None else defaults["filepath"]
        self.sender = sender if sender is not None else defaults["sender"]
        self.password = password if password is not None else defaults["password"]

        self.server = smtplib.SMTP(self.server, self.port)
        self.msg = MIMEMultipart()
        # If a password is given, use it to login to the mailserver
        if self.password != None:
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.sender, self.password)

        self.msg["From"] = self.sender

        # Check if user wants to send a file, if so read the specified file
        if self.sendfile == True:
            fp = open(self.filepath)
            attachment = MIMEText(fp.read())
            fp.close()
            # Attach the file to the message
            self.msg.attach(attachment)

    def send(self, subject, text, receipient):
        """ Send the mail
            Usage:
            instance.send(subject, text, [receipient1, receipent2])
            Or:
            instance.send(subject, text, receipient)
        """

        #.subject = subject
        #self.text = text
        #self.receipient = receipient

        # Set subject to mail
        self.msg["Subject"]  = subject

        # Set actual text of the email
        #body = text
        self.msg.attach(MIMEText(text, "plain"))

        # If given receipients is a list object cycle through list of receipients
        if type(receipient) == list:
            for email in receipient:
                # Set receipient in email header
                self.msg["To"] = email
                # Built the massage object
                message = self.msg.as_string()

                # Try to send mail
                try:
                    self.server.sendmail(self.sender, email, message)
                    self.server.quit()
                    print("Success: Sent email \""+subject+"\" from \""+self.sender+"\" to \""+email+"\"")
                except:
                    print("Error: Unable to send email \""+subject+"\" from \""+self.sender+"\" to \""+email+"\"")

        # If given receipients is not a list, just try to send the mail
        else:
            email = receipient
            # Set receipient in email header
            self.msg["To"] = email
            # Built the massage object
            message = self.msg.as_string()

            try:
                self.server.sendmail(self.sender, email, message)
                self.server.quit()
                print("Success: Sent email \""+subject+"\" from \""+self.sender+"\" to \""+email+"\"")
            except:
                print("Error: Unable to send email \""+subject+"\" from \""+self.sender+"\" to \""+email+"\"")
