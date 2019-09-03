#!/usr/bin/python3
#-*- coding: utf-8 -*-
import ldap, sys, os

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#myldap defaults
default_searchfilter="userPrincipalName"
default_dn="OU=OrgUnit,DC=example,DC=org"
default_ldap_server="example.org"

#mail defaults
default_mail_server="mailserver.example.org"
default_mail_port="25"
default_sendfile="false"
default_filepath="None"
default_sender="no-reply@example.org"
default_mail_password="None"

class myldap:
    def __init__(self, user, password, searchvalue, searchfilter=None, dn=None, server=None):
        """ Sort out the given variables and if neccessary fill in default variables

        Usage:
        Modify defaults in the class and use the minumum parameters:
        instance = myldap(username, password, searchvalue)

        or give all parameters:
        instance = myldap(username, password, searchvalue, searchfilter, dn, server)

        "searchvalue" is the value to match to the ldap object, usually "firstname.lastname@example.org"
        "searchfilter" is the ldap attribute to match the searchvalue to, usually "userPrincipalName"
        "dn" is the tree you want to start the search in, usually similar to "OU=OrgUnit,DC=example,DC=org"
        """

        self.searchfilter = searchfilter if searchfilter is not None else default_searchfilter
        self.dn = dn if dn is not None else default_dn
        self.server = server if server is not None else default_ldap_server

        self.user = user
        self.password = password
        self.searchvalue = searchvalue

    def query(self, attr):
        """Do the ldap query with the given variables

        Usage:
        result = instance.query(attribute)

        "attribute" is the value you want to get from the ldap object, for instance "pwdlastset"
        """

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
            print("Your username or password is incorrect.")
            sys.exit(0)
        except (ldap.LDAPError, e):
            if type(e.message) == dict and e.message.has_key('desc'):
                print(e.message['desc'])
            else:
                print(e)
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
        except (ldap.LDAPError, e):
                print(e)
        l.unbind_s()

class mail:
    def __init__(self, sender=None, server=None, port=None, sendfile=None, filepath=None, password=None):
        """ Sort out the given variables and if neccessary fill in default variables
            or give all parameters:
            instance = mail(sender, mailserver, port, true, "/path/to/file", password)
        """

        self.server = server if server is not None else default_mail_server
        self.port = port if port is not None else default_mail_port
        self.sendfile = sendfile if sendfile is not None else default_sendfile
        self.filepath = filepath if filepath is not None else default_filepath
        self.sender = sender if sender is not None else default_sender
        self.password = password if password is not None else default_mail_password

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


class file:
    def __init__(self, path, data=None):
        """Sort out path/filename.txt and data that is probalby written

        Usage:
        instance = file("/path/to/file.txt")
        instance = file("/path/to/file.txt", "data")
        """

        if os.path.exists(path) and os.path.isfile(path):
            self.path = path
        else:
            print("Given path/filename doesn't exist or not a file.")
            sys.exit(0)
        self.data = data if data is not None else ""

    def overwrite(self):
        """Overwrite the specified file
        """

        with open(self.path, "w", self.data) as file:
            file.write(self.data+"\n")
            file.close()
        return None

    def append(self):
        """Append to the end of the specified file
        """

        with open(self.path, "a", self.data) as file:
            file.write(self.data+"\n")
            file.close()
        return None

    def read(self):
        """Read the specified file
        """

        #TODO review/test
        with open(self.path, "r") as file:
            result = file.read()
            file.close()
        return result

    def readline(self):
        """Read the specified file line for line
        """

        #TODO review/test
        with open(self.path, "r") as file:
            result = file.readline()
            file.close()
        return result

    def create(self):
        """Create the specified file
        """

        #TODO review/test
        with open(self.path, "x") as file:
            file.write()
            file.close()
        return result
