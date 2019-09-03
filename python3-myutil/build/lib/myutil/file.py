#!/usr/bin/python3
#-*- coding: utf-8 -*-

class setup:
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
