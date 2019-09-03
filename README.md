# myutil
Small Project to write my own Python classes mainly for self-use.

My inital class attempt has all sorts of stuff in it.
Also i never really created a class on my own before, and that's what this mess looks like:
Too much in one class, the code is bad and the usage is a pain.

My first goal is to split off different functions to its own classes and use proper python class synthax.

Second goal (for now) is to convert a local Nagios check for Ceph Mimic, including performance data, from bash to python.
Why? Because i like Python and like to use it an improve. But also because i personally dont like bash.

Updates on further steps will most likely follow.

I will only focus on maintaining the python3 version!

# TODOs:
- python3-myutil
1. FILE: Modify so that you call the init method with just the path and all the methods where you need to,
   also the data (for instance: overwrite)
2. LDAP: Modify so that you just setup server etc. when calling the init method, and specifying all the
  non-persistent stuff at the query method (similar to mail) - done
3. Include logging instead / in addition to priting errors to std out
4. Maybe also add logging class (logzero)
5. Make default variables in "myutil_defaults" persistent over versions
6. Make package create its own folder in $HOME/.local/lib/python3.6/site-packages/ and collect all affected files there
   to keep it cleaned up - done

- MISC
1. jokes still has a bug in "random_choice" method
