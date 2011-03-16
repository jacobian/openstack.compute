__version__ = '2.0a1'

from openstack.compute.backup_schedules import (BackupSchedule, BackupScheduleManager, 
        BACKUP_WEEKLY_DISABLED, BACKUP_WEEKLY_SUNDAY, BACKUP_WEEKLY_MONDAY,
        BACKUP_WEEKLY_TUESDAY, BACKUP_WEEKLY_WEDNESDAY,
        BACKUP_WEEKLY_THURSDAY, BACKUP_WEEKLY_FRIDAY, BACKUP_WEEKLY_SATURDAY,
        BACKUP_DAILY_DISABLED, BACKUP_DAILY_H_0000_0200,
        BACKUP_DAILY_H_0200_0400, BACKUP_DAILY_H_0400_0600,
        BACKUP_DAILY_H_0600_0800, BACKUP_DAILY_H_0800_1000,
        BACKUP_DAILY_H_1000_1200, BACKUP_DAILY_H_1200_1400,
        BACKUP_DAILY_H_1400_1600, BACKUP_DAILY_H_1600_1800,
        BACKUP_DAILY_H_1800_2000, BACKUP_DAILY_H_2000_2200,
        BACKUP_DAILY_H_2200_0000)
from openstack.compute.client import ComputeClient
from openstack.compute.exceptions import (ComputeException, BadRequest, Unauthorized,
    Forbidden, NotFound, OverLimit)
from openstack.compute.flavors import FlavorManager, Flavor
from openstack.compute.images import ImageManager, Image
from openstack.compute.ipgroups import IPGroupManager, IPGroup
from openstack.compute.servers import ServerManager, Server, REBOOT_HARD, REBOOT_SOFT

class Compute(object):
    """
    Top-level object to access the OpenStack Compute API.
    
    Create an instance with your creds::
    
    >>> compute = Compute(USERNAME, API_KEY)
        
    Then call methods on its managers::
    
        >>> compute.servers.list()
        ...
        >>> compute.flavors.list()
        ...
        
    &c.
    """
    
    def __init__(self, username, apikey, auth_url=None, user_agent=None):
        self.backup_schedules = BackupScheduleManager(self)
        self.client = ComputeClient(username, apikey, auth_url, user_agent)
        self.flavors = FlavorManager(self)
        self.images = ImageManager(self)
        self.ipgroups = IPGroupManager(self)
        self.servers = ServerManager(self)
        
    def authenticate(self):
        """
        Authenticate against the server.
        
        Normally this is called automatically when you first access the API,
        but you can call this method to force authentication right now.
        
        Returns on success; raises :exc:`~openstack.compute.Unauthorized` if
        the credentials are wrong.
        """
        self.client.authenticate()