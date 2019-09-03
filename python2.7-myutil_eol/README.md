# How to install?
apt install python-pip

wget https://github.com/juposs/python/tree/master/python2.7/myutil/dist/myutil.py-1.0-py2-none-any.whl

pip install ./myutil.py-1.0-py2-none-any.whl --user

# Defaults
Defaults can be modified in $HOME/.local/lib/python2.7/site-packages/myutil.py

# Usage:

    ldap:
        from myutil import myldap

        Modify defaults and use the minumum parameters:
        instance = myldap("binduser@example.org", "strongpass", "john.doe@example.org")

        or give all parameters:
        instance = myldap("binduser@example.org", "strongpass", "john.doe@example.org", "userPrincipalName", "OU=OrgUnit,DC=example,DC=org", "server.example.org")

        then run query with that instance:
        result = instance.query("pwdlastset")
        result2 = instance.query("extensionAttribute12")

        This will search for ldap object where userPrincipalName equals john.doe@example.org and return the value of pwdlastlet to the variable "result" and return whatever is in extensionAttribute12 to variable "result2"

    mail:
        from myutil import mail

        Modify defaults and use the minumum parameters:
        instance = mail()

        or give all parameters:
        instance = mail("no-rely@example.org", "mailserver.example.org", "25", true, "/path/to/myfile.txt")
        instance = mail("no-rely@example.org", "mailserver.example.org", "25", false)

        then send the mail with that instance:
        instance.send(subject, text, [receipient1, receipient2])

    file:
        from myutil import file

        Without data, for instance you just want to read/create a file
        instance = file("path/to/file.txt")

        With data, for instance if you want to write/append/overwrite a file
        instance = file("/path/to/file", "your data")

        instance.overwrite()
