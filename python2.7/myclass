#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import gmtime, strftime
import ldap
 
# LDAP variables: server,user,password,dn,searchfilter(eg upn),searchvalue,attribute (the value you want to know)
# example:
# fill dictionary at least with: user, password, searchvalue, attribute
# info = {}
# info["server"]="example.org"
# info["user"]="serviceaccountname"
# ...
# call the method:
# example_pyton.ldapquery(info)
# fill dictionary with key "help" to get optional values printed
 
# DEPRECATED:
# example_python.ldapquery("example.org","server.service","strongpass","OU=OrgUnit,DC=example,DC=org","userPrincipalName","firstname.lastname@example.org","useraccountcontrol")
 
 
# Write_File variables: path, mode (w=(over)write;a=append), data
# example: example_python.writefile("/root/jpo/example", "w", "filename")
 
 
# sendmail variables: server,port,sender ("Someting <no-reply@service.example.com>"),subject,sendfile (true/false),filepath,text,receipient
# fill dictionary at least with sender, subject, text, receipient
# fill dictionary with key "help" to get optional values printed
 
# DECRECATED:
# example: example_python.sendmail("mailserver.example.org","25","DisplayName <no-reply@service.example.com>","YourSubject","true","/root/jpo/example","filename","firstname.lastname@example.org")
 
def ldapquery(info):
# Force user to specify at least the minimum required values: user, password, searchvalue, attribute
        if "user" not in info.keys():
                print "LDAPQUERY: Please specify a bind user as key \"user\""
        if "password" not in info.keys():
                print "LDAPQUERY: Please specify the bind user password as key \"password\""
        if "searchvalue" not in info.keys():
                print "LDAPQUERY: Please specify a search value (eg e-mail-address) as key \"searchvalue\""
        if "attribute" not in info.keys():
                print "LDAPQUERY: Please specify an attribute (the attribute you are looking for) as key \"attribute\""
 
# Remind user of optional values: server, dn, searchfile
        if "help" in info.keys():
                print "LDAPQUERY: You may want to specify \"server\" (default:example.org), \"dn\" (default:OU=OrgUnit,DC=example,DC=org) or \"searchfilter\" (default:userPrincipalName) as well"
 
# Exit, if minimum required values are not given
        if "user" not in info.keys() or "password" not in info.keys() or "searchvalue" not in info.keys() or "attribute" not in info.keys():
                sys.exit(0)
 
# Get all values out of the dictionary, use default for optional values if they are not specified
        server = info.get("server","example.org")
        user = info.get("user","")
        password = info.get("password","")
        dn = info.get("dn","OU=OrgUnit,DC=example,DC=org")
        searchfilter = info.get("searchfilter","userPrincipalName")
        searchvalue = info.get("searchvalue","")
        attribute = info.get("attribute","")
 
        value_parsed = {}
        l = ldap.initialize('ldaps://'+server)
        binddn = user
        pw = password
        basedn = dn
        searchFilter = searchfilter+"="+searchvalue
        searchAttribute = [attribute]
# Run ldap query
        #this will scope the entire subtree under UserUnits
        searchScope = ldap.SCOPE_SUBTREE
        #Bind to the server
        try:
                l.protocol_version = ldap.VERSION3
                l.simple_bind_s(binddn, pw)
        except ldap.INVALID_CREDENTIALS:
          print "Your username or password is incorrect."
        #  sys.exit(0)
        except ldap.LDAPError, e:
          if type(e.message) == dict and e.message.has_key('desc'):
                  print e.message['desc']
          else:
                  print e
        #  sys.exit(0)
        try:
                ldap_result_id = l.search(basedn, searchScope, searchFilter, searchAttribute)
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
                if attribute in value_parsed.keys():
                        ldap_value = value_parsed[attribute]
                        return ldap_value[0]
                else:
                        return "undefined"
        except ldap.LDAPError, e:
                print e
        l.unbind_s()
 
def writefile(path,mode,data):
        with open(path, mode) as file:
                file.write(data+"\n")
                file.close()
 
def sendmail(info):
# Force user to speficy at least the minimum required values: sender, subject, text, receipient
        if "sender" not in info.keys():
                print "SENDMAIL: Please specify a sender (email) as key \"sender\""
        if "subject" not in info.keys():
                print "SENDMAIL: Please specify a subject as key \"subject\""
        if "text" not in info.keys():
                print "SENDMAIL: Please specify a text as key \"text\""
        if "receipient" not in info.keys():
                print "SENDMAIL: Please specify a receipient (email) as key \"receipient\""
 
# Remind user of optional values: server, port, sendfile, filepath
        if "help" in info.keys():
                print "SENDMAIL: You may want to specify \"server\" (default:mailserver.example.org), \"port\" (default:25), \"sendfile\" (default:false) or \"filepath\" (default:None) as well"
 
# Exit, if minimum required values are not given
        if "sender" not in info.keys() or "subject" not in info.keys() or "text" not in info.keys() or "receipient" not in info.keys():
                sys.exit(0)
 
# Get all values out of the dictionary, use default for optional values if they are not specified
        server = info.get("server","mailserver.example.org")
        port = info.get("port","25")
        sender = info.get("sender","")
        subject = info.get("subject","")
        sendfile = info.get("sendfile","false")
        filepath = info.get("filepath","None")
        text = info.get("text","")
        receipient = info.get("receipient","")
 
# Build the mail
        try:
                server = smtplib.SMTP(server, port)
                msg = MIMEMultipart()
                msg["From"] = sender
                msg["To"] = receipient
                msg["Subject"]  = subject
                filetosend = filepath
 
                if sendfile.lower() == "true":
                        fp = open(filetosend)
                        attachment = MIMEText(fp.read())
                        fp.close()
 
                       body = text
                        msg.attach(MIMEText(body, "plain"))
                        msg.attach(attachment)
 
                elif sendfile.lower() == "false":
                        body = text
                        msg.attach(MIMEText(body, "plain"))
                message = msg.as_string()
# Send mail
                server.sendmail(sender, receipient, message)
                print "Successfully send mail(s)"
        except:
                print "Error: unable to send mail"
