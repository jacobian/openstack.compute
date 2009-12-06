from __future__ import absolute_import

__version__ = ('1.0a1')

from .backup_schedules import (BackupSchedule, BackupScheduleManager, 
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
from .client import CloudServersClient
from .exceptions import (CloudServersException, BadRequest, Unauthorized,
    Forbidden, NotFound, OverLimit)
from .flavors import FlavorManager, Flavor
from .images import ImageManager, Image
from .ipgroups import IPGroupManager, IPGroup
from .servers import ServerManager, Server, REBOOT_HARD, REBOOT_SOFT

class CloudServers(object):
    def __init__(self, username, apikey):
        self.backup_schedules = BackupScheduleManager(self)
        self.client = CloudServersClient(username, apikey)
        self.flavors = FlavorManager(self)
        self.images = ImageManager(self)
        self.ipgroups = IPGroupManager(self)
        self.servers = ServerManager(self)
        
    def authenticate(self):
        self.client.authenticate()