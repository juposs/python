# python
Small Project to write my own Python classes mainly for self-use.

My inital class attempt has all sorts of stuff in it.
Also i never really created a class on my own before, and that's what this mess looks like:
Too much in one class, the code is bad and the usage is a pain.

My first goal is to split off different functions to its own classes and use proper python class synthax.

Second goal (for now) is to convert a local Nagios check for Ceph Mimic, including performance data, from bash to python.
Why? Because i like Python and like to use it an improve. But also because i personally dont like bash.

Updates on further steps will most likely follow.

Needed modules/packages for classes in myutil:

    ladp:
        python-ldap
    mail:
        mimetypes
        #Figure out the actual package name
        MIMEMultipart?
        MIMEText?
    file:
        none

Usage for the classes:

    ldap:
        from myutil import ldap
        ldapsearch = ldap(user="binduser@example.org", password="strongpass", searchvalue="firstname.lastname@example.org", attr="extensionattribute12")
        
        result = ldapsearch.query()

    mail:
        from myutil import mail
        sendmail = mail(subject="ExampleSubject", text="Example text", receipient="firstname.lastname@example.org")

        sendmail.sendmail()

    file:
        from myutil import file
        file1 = file("/path/to/file", "your data")

        file1.read()

myutil is still experimental and needs to be tested!