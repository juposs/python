#!/usr/bin/python
#-*- coding: utf-8 -*-
import ldap, sys

import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class myldap:
    std_srv = "example.org"
    std_dn = "OU=OrgUnit,DC=example,DC=org"
    std_searchfilter = "userPrincipalName"

    def __init__(self, server, dn, searchfilter, user, password, searchvalue, attr):
        # Sort out the given variables and if neccessary fill in default variables
        if server is "":
            self.server = std_srv
        else:
            self.server = server

        if dn is "":
            self.dn = std_dn
        else:
            self.dn = dn

        if searchfilter is "":
            self.searchfilter = std_searchfilter
        else:
            self.searchfilter = searchfilter

        self.user = user
        self.password = password
        self.searchvalue = searchvalue
        self.attr = attr

    def query(self):
        """Do the ldap query with the given variables"""
        value_parsed = {}
        l = ldap.initialize('ldaps://'+self.server)
        searchFilter = self.searchfilter+"="+self.searchvalue
        searchAttribute = [self.attr]

        searchScope = ldap.SCOPE_SUBTREE
        #Bind to the server
        try:
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s(self.user, self.password)
        except ldap.INVALID_CREDENTIALS:
            print "Your username or password is incorrect."
            sys.exit(0)
        except ldap.LDAPError, e:
            if type(e.message) == dict and e.message.has_key('desc'):
                print e.message['desc']
            else:
                print e
            #sys.exit(0)
        try:
            ldap_result_id = l.search(self.dn, searchScope, searchFilter, searchAttribute)
            result_set = []
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    ## if you are expecting multiple results you can append them
                    ## otherwise you can just wait until the initial result and break out
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)
                if len(result_set) == 0:
                        return None
                # Split the specified attribute out
                dn, value = result_set[0][0]
                for each in value.keys():
                    value_parsed[each.lower()] = value[each]

                if searchAttribute[0] in value_parsed.keys():
                    ldap_value = value_parsed[searchAttribute[0]]

                    if ldap_value[0] == "":
                        query()
                    else:
                        return ldap_value[0]
                else:
                    return "not found"
        except ldap.LDAPError, e:
                print e
        l.unbind_s()

class mail:
    std_srv = "mailserver.example.org"
    std_port = "25"
    std_sendfile = "false"
    std_filepath = None
    std_sender = "no-reply@example.org"

    def __init__(self, server, port, sendfile, filepath, sender, subject, text, receipient):
        # Sort out the given variables and if neccessary fill in default variables
        if server is "":
            self.server = std_srv
        else:
            self.server = server

        if port is "":
            self.port = std_port
        else:
            self.port = port

        if sendfile is "":
            self.sendfile = std_sendfile
        else:
            self.sendfile = sendfile

        if filepath is "":
            self.filepath = std_filepath
        else:
            self.filepath = filepath

        if sender is "":
            self.sender = std_sender
        else:
            self.sender = sender

        self.subject = subject
        self.text = text
        self.receipient = receipient

    def send(self):
        """Send mail"""

        server = smtplib.SMTP(self.server, self.port)
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.receipient
        msg["Subject"]  = self.subject

        body = self.text
        msg.attach(MIMEText(body, "plain"))

        # Check if user wants to send a file, if so read the specified file and attach it to the message
        if self.sendfile.lower() == "true":
            fp = open(self.filepath)
            attachment = MIMEText(fp.read())
            fp.close()

            msg.attach(attachment)

        message = msg.as_string()

        # Try to send mail
        try:
            server.sendmail(self.sender, self.receipient, message)
            print "Successfully send mail(s)"
        except:
            print "Error: unable to send mail"

class file:
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def overwrite(self):
        """Overwrite the specified file"""
        with open(self.path, "w", self.data) as file:
            file.write(self.data+"\n")
            file.close()
        return None

    def append(self):
        """Append to the end of the specified file"""
        with open(self.path, "a", self.data) as file:
            file.write(self.data+"\n")
            file.close()
        return None

    def read(self):
        """Read the specified file"""
        #TODO review/test
        with open(self.path, "r") as file:
            result = file.read()
            file.close()
        return result

    def readline(self):
        """Read the specified file line for line"""
        #TODO review/test
        with open(self.path, "r") as file:
            result = file.readline()
            file.close()
        return result

    def create(self):
        """Create the specified file"""
        #TODO review/test
        with open(self.path, "x") as file:
            file.write()
            file.close()
        return result

