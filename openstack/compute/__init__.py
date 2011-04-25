__version__ = '2.0a1'

import os
import ConfigParser
from distutils.util import strtobool
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
from openstack.compute.api import API_OPTIONS

DEFAULT_CONFIG_FILE = os.path.expanduser('~/.openstack/compute.conf')

class Compute(object):
    """
    Top-level object to access the OpenStack Compute API.

    Create an instance with your creds::

    >>> compute = Compute(username=USERNAME, apikey=API_KEY)

    Then call methods on its managers::

        >>> compute.servers.list()
        ...
        >>> compute.flavors.list()
        ...

    &c.
    """

    def __init__(self, **kwargs):
        self.config = self._get_config(kwargs)
        self.backup_schedules = BackupScheduleManager(self)
        self.client = ComputeClient(self.config)
        self.flavors = FlavorManager(self)
        self.images = ImageManager(self)
        self.servers = ServerManager(self)
        if 'IPGROUPS' in API_OPTIONS[self.config.cloud_api]:
            self.ipgroups = IPGroupManager(self)

    def authenticate(self):
        """
        Authenticate against the server.

        Normally this is called automatically when you first access the API,
        but you can call this method to force authentication right now.

        Returns on success; raises :exc:`~openstack.compute.Unauthorized` if
        the credentials are wrong.
        """
        self.client.authenticate()

    def _get_config(self, kwargs):
        """
        Get a Config object for this API client.

        Broken out into a seperate method so that the test client can easily
        mock it up.
        """
        return Config(
            config_file = kwargs.pop('config_file', None),
            env = kwargs.pop('env', None),
            overrides = kwargs,
        )

class Config(object):
    """
    Encapsulates getting config from a number of places.

    Config passed in __init__ overrides config found in the environ, which
    finally overrides config found in a config file.
    """

    DEFAULTS = {
        'username': None,
        'apikey': None,
        'auth_url': "https://auth.api.rackspacecloud.com/v1.0",
        'user_agent': 'python-openstack-compute/%s' % __version__,
        'allow_cache': False,
        'cloud_api' : 'RACKSPACE',
    }

    def __init__(self, config_file, env, overrides, env_prefix="OPENSTACK_COMPUTE_"):
        config_file = config_file or DEFAULT_CONFIG_FILE
        env = env or os.environ

        self.config = self.DEFAULTS.copy()
        self.update_config_from_file(config_file)
        self.update_config_from_env(env, env_prefix)
        self.config.update(dict((k,v) for (k,v) in overrides.items() if v is not None))
        self.apply_fixups()

    def __getattr__(self, attr):
        try:
            return self.config[attr]
        except KeyError:
            raise AttributeError(attr)

    def update_config_from_file(self, config_file):
        """
        Update the config from a .ini file.
        """
        configparser = ConfigParser.RawConfigParser()
        if os.path.exists(config_file):
            configparser.read([config_file])

        # Mash together a bunch of sections -- "be liberal in what you accept."
        for section in ('global', 'compute', 'openstack.compute'):
            if configparser.has_section(section):
                self.config.update(dict(configparser.items(section)))

    def update_config_from_env(self, env, env_prefix):
        """
        Update the config from the environ.
        """
        for key, value in env.iteritems():
            if key.startswith(env_prefix):
                key = key.replace(env_prefix, '').lower()
                self.config[key] = value

    def apply_fixups(self):
        """
        Fix the types of any updates based on the original types in DEFAULTS.
        """
        for key, value in self.DEFAULTS.iteritems():
            if isinstance(value, bool) and not isinstance(self.config[key], bool):
                self.config[key] = strtobool(self.config[key])
