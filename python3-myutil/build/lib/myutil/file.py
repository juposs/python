#!/usr/bin/python3
#-*- coding: utf-8 -*-

class File:
    def __init__(self, path):
        """Sort out path/filename

        Usage:
        from myutil import File
        your_file = File("/path/to/file.txt")
        """

    def overwrite(self, data):
        """Overwrite the specified file
        """
        self.data = data

        if os.path.exists(self.path) and os.path.isfile(self.path):
            print("Overwriting file "+self.path)
        else:
            print("Given path/filename doesn't exist yet, or not a file. Writing anyways..")

        with open(self.path, "w", self.data) as file:
            file.write(self.data+"\n")
            file.close()
        return None

    def append(self, data):
        """Append to the end of the specified file
        """
        self.data = data

        if os.path.exists(self.path) and os.path.isfile(self.path):
            print("Appending file "+self.path)
        else:
            print("Given path/filename doesn't exist yet, or not a file. Writing anyways..")

        with open(self.path, "a", self.data) as file:
            file.write(self.data+"\n")
            file.close()
        return None

    def read(self):
        """Read the specified file
        """
        if os.path.exists(self.path) and os.path.isfile(self.path):
            with open(self.path, "r") as file:
                result = file.read()
                file.close()
            return result
        else:
            print("Given path/filename doesn't exist or not a file. Exiting..")
            sys.exit(0)

    def readline(self):
        """Read the specified file line for line
        """
        if os.path.exists(self.path) and os.path.isfile(self.path):
            with open(self.path, "r") as file:
                result = file.readline()
                file.close()
            return result
        else:
            print("Given path/filename doesn't exist or not a file. Exiting..")
            sys.exit(0)

    def create(self):
        """Create the specified file
        """
        if os.path.exists(self.path) and os.path.isfile(self.path):
            print("Given path/filename does already exist. Exiting.. ")
            sys.exit(0)
        else:
            with open(self.path, "x") as file:
                file.write()
                file.close()
            return None
