import setuptools

#optional = ['ansicolors', 'mock>=1.0.1']

requires = ['python3-ldap']

setuptools.setup(
     name='myutil.py',
     version='2.2',
     py_modules=['myutil', 'myutil_defaults'],
     author="Julian Poss",
     author_email="john.doe@gmail.com",
     description="A python utility package",
     long_description="A python utility package for querying ldap, sending mails and working with files",
     long_description_content_type="text/markdown",
     url="https://github.com/juposs/python/tree/master/python3/myutil",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3.6",
         "License :: OSI Approved :: undefined",
         "Operating System :: OS Independent",
     ],
     install_requires=requires
 )
