import setuptools

#optional = ['ansicolors', 'mock>=1.0.1']

requires = ['python3-ldap', 'logzero']

setup_kwargs = {'packages': ["myutil"],
                'package_dir': {'': "."}}

setuptools.setup(
     name='myutil',
     version='3.2',
     #py_modules=['myutil', 'myutil_defaults'],
     #package_dir={"":"."},
     download_url="",
     author="Julian Poss",
     author_email="john.doe@gmail.com",
     maintainer="Julian Poss",
     maintainer_email="john.doe@gmail.com",
     description="A python utility package",
     long_description="A python utility package for querying ldap, sending mails and working with files",
     #long_description_content_type="text/markdown",
     url="https://github.com/juposs/python/tree/master/python3-myutil",
     #packages=setuptools.find_packages(),
     classifiers=[
         'Operating System :: Microsoft :: Windows',
         'Operating System :: POSIX :: Linux',
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: undefined",
         "Operating System :: OS Independent",
         'Topic :: Software Development :: Libraries :: Python Modules',
         'Topic :: System :: Systems Administration :: MISC Tools'
     ],
     install_requires=requires,
      **setup_kwargs
 )
