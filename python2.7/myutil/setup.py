import setuptools

#optional = ['ansicolors', 'mock>=1.0.1']

requires = ['python-ldap']

setuptools.setup(
     name='myutil',
     version='1.0',
     scripts=['myutil'] ,
     author="Julian Poss",
     author_email="john.doe@gmail.com",
     description="A python utility package",
     long_description="A python utility package for querying ldap, sending mails and working with files",
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 2.7",
         "License :: OSI Approved :: undefined",
         "Operating System :: OS Independent",
     ],
     install_requires=requires
 )
