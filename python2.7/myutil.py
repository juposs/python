#!/usr/bin/python
#-*- coding: utf-8 -*-
import ldap, sys

import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class myldap:
    def __init__(self, user, password, searchvalue, searchfilter=None, dn=None, server=None):
        # Sort out the given variables and if neccessary fill in default variables
        self.searchfilter = searchfilter if searchfilter is not None else "userPrincipalName"
        self.dn = dn if dn is not None else "OU=OrgUnit,DC=example,DC=org"
        self.server = server if server is not None else "example.org"

        self.user = user
        self.password = password
        self.searchvalue = searchvalue

    def query(self, attr):
        """Do the ldap query with the given variables"""
        
        self.attr = attr
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
    def __init__(self, subject, text, receipient, server=None, port=None, sendfile=None, filepath=None, sender=None):
        # Sort out the given variables and if neccessary fill in default variables
        self.server = server if server is not None else "mailserver.example.org"
        self.port = port if port is not None else "25"
        self.sendfile = sendfile if sendfile is not None else "false"
        self.filepath = filepath if filepath is not None else "None"
        self.sender = sender if sender is not None else "no-reply@example.org"

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
