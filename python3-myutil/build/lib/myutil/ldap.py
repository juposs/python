#!/usr/bin/python3
#-*- coding: utf-8 -*-
import ldap, sys, os, json

# Import default vars
from myutil import defaults
defaults = defaults.ldap

home = os.path.expanduser("~")
user_settings_file = os.path.join(home, "myutil_settings.json")

defaults = dict(defaults)

if os.path.exists(user_settings_file):
    with open(user_settings_file) as file:
        user_defaults = json.load(file)["ldap"]
    defaults.update(user_defaults)

class Ldap:
    def __init__(self, user, password, dn=None, server=None, port=None):
        """ Sort out the given variables and if neccessary fill in default variables

        Usage:
        Modify defaults in the class and use the minumum parameters:
        from myutil import Ldap
        instance = Ldap(username, password)

        or give all parameters:
        instance = Ldap(username, password, dn, server, port)

        "dn" is the tree you want to start the search in, usually similar to "OU=OrgUnit,DC=example,DC=org"
        """

        self.dn = dn if dn is not None else defaults["dn"]
        self.server = server if server is not None else defaults["server"]
        self.port = port if port is not None else defaults["port"]

        self.user = user
        self.password = password


    def query(self, match_value, return_attribute, match_attribute=None):
        """Do the ldap query with the given variables

        Usage:
        result = instance.query(searchvalue, returnattribute, match_attribute=None)

        "match_value" is  the value to match to the ldap object, usually "firstname.lastname@example.org"
        "return_attribute" is the value you want to get from the ldap object, for instance "pwdlastset"
        "match_attribute" is the ldap attribute to match the "match_value" to, defaults to "userPrincipalName"
        """

        self.match_attribute = match_attribute if match_attribute is not None else defaults["match_attribute"]

        value_parsed = {}
        l = ldap.initialize('ldaps://'+self.server)
        searchFilter = self.match_attribute+"="+match_value
        searchAttribute = [return_attribute]

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
                        query(match_value, return_attribute, match_attribute)
                    else:
                        return ldap_value[0]
                else:
                    return "not found"
        except (ldap.LDAPError, e):
                print(e)
        l.unbind_s()
