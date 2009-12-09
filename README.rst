Python bindings to the Rackspace Cloud Servers API
==================================================

This is a client for Rackspace's Cloud Servers API. There's a Python API (the
``cloudservers`` module), and a command-line script (``cloudservers``).

Right now, the Python API implements 100% of the Cloud Servers API, and has
nearly 100% test coverage. In other words, it works, and well. The
command-line script is still under development and only supports about half of
the API.

`Documentation is available`__, but still somewhat rudimentary. See for some
reference material.

__ http://packages.python.org/python-cloudservers/

By way of a quick-start::

    >>> import cloudservers
    >>> cs = cloudservers.CloudServers(USERNAME, API_KEY)
    >>> cs.flavors.list()
    [...]
    >>> cs.servers.list()
    [...]
    >>> s = cs.servers.create(image=2, flavor=1, name='myserver')
    
    ... time passes ...
    
    >>> s.reboot()
    
    ... time passes ...
    
    >>> s.delete()
    
You'll also probably want to read `Rackspace's API guide`__ (PDF) -- the first
bit, at least -- to get an idea of the concepts. Rackspace is doing the cloud
hosting thing a bit differently from Amazon, and if you get the concepts this
library should make more sense.

__ http://docs.rackspacecloud.com/servers/api/cs-devguide-latest.pdf

FAQ
===

What's wrong with libcloud?

    Nothing! However, as a cross-service binding it's by definition lowest
    common denominator; I needed access to the Rackspace-specific APIs (shared
    IP groups, image snapshots, resizing, etc.). I also wanted a command-line
    utility.
    
