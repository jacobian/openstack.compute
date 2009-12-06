Backup schedules reference
==========================

.. currentmodule:: cloudservers

Rackspace allows scheduling of weekly and/or daily backups for virtual
servers. You can access these backup schedules either off the API object as
:attr:`CloudServers.backup_schedules`, or directly off a particular
:class:`Server` instance as :attr:`Server.backup_schedule`.

.. autoclass:: BackupScheduleManager
   :members: create, delete, update, get
   
.. autoclass:: BackupSchedule
   :members: update, delete