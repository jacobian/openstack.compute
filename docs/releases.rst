=============
Release notes
=============

2.0 (TBD)
=========

* **Major renaming**: the library is now called ``openstack.compute`` to
  reflect that Rackspace Cloud is just one instance of the open source
  project. This ripples to a lot of places:
  
    * The library is now called ``openstack.compute`` instead of
      ``cloudservers``, and the main API entry point is now
      ``openstack.compute.Compute`` instead of ``cloudservers.CloudServers``.

    * The shell program is now ``openstack-compute`` instead of
      ``cloudservers``. Yes, the name's a lot longer. Use ``alias``.
      
    * The env variables are now ``OPENSTACK_COMPUTE_USERNAME`` and
      ``OPENSTACK_COMPUTE_API_KEY``.

1.2 (August 15, 2010)
=====================

* Support for Python 2.4 - 2.7.

* Improved output of :program:`cloudservers ipgroup-list`.

* Made ``cloudservers boot --ipgroup <name>`` work (as well as ``--ipgroup
  <id>``).

1.1 (May 6, 2010)
=================

* Added a ``--files`` option to :program:`cloudservers boot` supporting
  the upload of (up to five) files at boot time.
  
* Added a ``--key`` option to :program:`cloudservers boot` to key the server
  with an SSH public key at boot time. This is just a shortcut for ``--files``,
  but it's a useful shortcut.
  
* Changed the default server image to Ubuntu 10.04 LTS.