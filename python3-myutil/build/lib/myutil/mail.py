#!/usr/bin/python3
#-*- coding: utf-8 -*-

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from myutil import defaults as myutil_defaults

class setup:
    def __init__(self, sender=None, server=None, port=None, sendfile=None, filepath=None, password=None):
        """ Sort out the given variables and if neccessary fill in default variables
            or give all parameters:
            instance = mail(sender, mailserver, port, true, "/path/to/file", password)
        """

        self.server = server if server is not None else myutil_defaults.default_mail_server
        self.port = port if port is not None else myutil_defaults.default_mail_port
        self.sendfile = sendfile if sendfile is not None else myutil_defaults.default_sendfile
        self.filepath = filepath if filepath is not None else myutil_defaults.default_filepath
        self.sender = sender if sender is not None else myutil_defaults.default_sender
        self.password = password if password is not None else myutil_defaults.default_mail_password

        self.server = smtplib.SMTP(self.server, self.port)
        self.msg = MIMEMultipart()
        # If a password is given, use it to login to the mailserver
        if self.password != None:
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.sender, self.password)

        self.msg["From"] = self.sender

        # Check if user wants to send a file, if so read the specified file
        if self.sendfile.lower() == "true":
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
