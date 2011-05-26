The :mod:`openstack.compute` Python API
=======================================

.. module:: openstack.compute
   :synopsis: A client for the OpenStack Compute API.

.. currentmodule:: openstack.compute

Usage
-----

First create an instance of :class:`Compute` with your credentials::

    >>> from openstack.compute import Compute
    >>> compute = Compute(username=USERNAME, apikey=API_KEY)

Then call methods on the :class:`Compute` object:

.. class:: Compute

    .. attribute:: backup_schedules

        A :class:`BackupScheduleManager` -- manage automatic backup images.

    .. attribute:: flavors

        A :class:`FlavorManager` -- query available "flavors" (hardware
        configurations).

    .. attribute:: images

        An :class:`ImageManager` -- query and create server disk images.

    .. attribute:: ipgroups

        A :class:`IPGroupManager` -- manage shared public IP addresses.

    .. attribute:: servers

        A :class:`ServerManager` -- start, stop, and manage virtual machines.

    .. automethod:: authenticate

For example::

    >>> compute.servers.list()
    [<Server: buildslave-ubuntu-9.10>]

    >>> compute.flavors.list()
    [<Flavor: 256 server>,
     <Flavor: 512 server>,
     <Flavor: 1GB server>,
     <Flavor: 2GB server>,
     <Flavor: 4GB server>,
     <Flavor: 8GB server>,
     <Flavor: 15.5GB server>]

    >>> compute.images.list()
    [<Image: Windows Server 2008 R2 x64 - MSSQL2K8R2>,...]

    >>> fl = compute.flavors.find(ram=512)
    >>> im = compute.images.find(name='Ubuntu 10.10 (maverick)')
    >>> compute.servers.create("my-server", image=im, flavor=fl)
    <Server: my-server>

For more information, see the reference:

.. toctree::
   :maxdepth: 2

   ref/index
