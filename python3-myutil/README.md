# How to install?

apt install python3-pip

wget https://github.com/juposs/python/raw/master/python3-myutil/dist/myutil-3.0-py3-none-any.whl

pip3 install ./myutil.py-3.0-py2-none-any.whl --user

# Defaults
Custom defaults can be stored in $HOME/myutil_settings.json

See "myutil_settings.json_example"

Everything that is not defined in $HOME/myutil_settings.json will get read from

"$HOME/.local/lib/python3.X/site-packages/myutil/defaults.py"

# Usage:

    ldap:
        from myutil import ldap

        Modify defaults and use the minumum parameters:
        instance = ldap.setup("binduser@example.org", "strongpass", "john.doe@example.org")

        or give all parameters:
        instance = ldap.setup("binduser@example.org", "strongpass", "john.doe@example.org", "userPrincipalName", "OU=OrgUnit,DC=example,DC=org", "server.example.org")

        then run query with that instance:
        result = instance.query("pwdlastset")
        result2 = instance.query("extensionAttribute12")

        This will search for ldap object where userPrincipalName equals john.doe@example.org and return the value of pwdlastlet to the variable "result" and return whatever is in extensionAttribute12 to variable "result2"

    mail:
        from myutil import mail

        Modify defaults and use the minumum parameters:
        instance = mail.setup()

        or give all parameters:
        instance = mail.setup("no-rely@example.org", "mailserver.example.org", "25", true, "/path/to/myfile.txt")
        instance = mail.setup("no-rely@example.org", "mailserver.example.org", "25", false)

        then send the mail with that instance:
        instance.send(subject, text, receipient1 [, receipient2])

    file:
        from myutil import file

        Without data, for instance you just want to read/create a file
        instance = file.setup("path/to/file.txt")

        With data, for instance if you want to write/append/overwrite a file
        instance = file.setup("/path/to/file", "your data")

        instance.overwrite()

    logging:
        from myutil import logger

        Modify defaults and use the minumum parameters:
        log1 = logger.setup()

        or give all parameters:
        log1 = loggger.setup("/path/to/logfile", maxBytes=1000, backupCount=10)

        Logfile will rotate after reaching maxBytes, default is '0', never rotate
        If rotation enabled, it will keep 'backupCount' files, default is 10

        then log stuff:
        log1.info("info")
        log1.warning("Warning")
        log1.error("Error")
        log1.debug("Debug")
