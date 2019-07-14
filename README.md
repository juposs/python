# myutil
Small Project to write my own Python classes mainly for self-use.

My inital class attempt has all sorts of stuff in it.
Also i never really created a class on my own before, and that's what this mess looks like:
Too much in one class, the code is bad and the usage is a pain.

My first goal is to split off different functions to its own classes and use proper python class synthax.

Second goal (for now) is to convert a local Nagios check for Ceph Mimic, including performance data, from bash to python.
Why? Because i like Python and like to use it an improve. But also because i personally dont like bash.

Updates on further steps will most likely follow.

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
        instance = mail(subject, text, receipient)

        or give all parameters:
        instance = mail("ExampleSubject", "example text", "john.doe@example.org", "no-rely@example.org", "mailserver.example.org", "25", true, "/path/to/myfile.txt")
        instance = mail("ExampleSubject", "example text", "john.doe@example.org", "no-rely@example.org", "mailserver.example.org", "25", false)

        then send the mail with that instance:
        instance.send()

    file:
        from myutil import file

        Without data, for instance you just want to read/create a file
        instance = file("path/to/file.txt")

        With data, for instance if you want to write/append/overwrite a file
        instance = file("/path/to/file", "your data")

        instance.read()

myutil is still experimental and needs to be tested!
