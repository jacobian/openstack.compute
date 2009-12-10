from __future__ import absolute_import

import os
import mock
from cloudservers.shell import CloudserversShell, CommandError
from .fakeserver import FakeServer

# Patch os.environ to avoid required auth info.
def setup():
    global _old_env
    fake_env = {
        'CLOUD_SERVERS_USERNAME': 'username',
        'CLOUD_SERVERS_API_KEY': 'password'
    }
    _old_env, os.environ = os.environ, fake_env

    # Make a fake shell object, a helping wrapper to call it, and a quick way
    # of asserting that certain API calls were made.
    global shell, _shell, assert_called
    _shell = CloudserversShell()
    _shell._api_class = FakeServer
    assert_called = lambda m, u: _shell.cs.assert_called(m, u)
    shell = lambda cmd: _shell.main(cmd.split())

def teardown():
    global _old_env
    os.environ = _old_env

def test_backup_schedule():
    shell('backup-schedule 1234')
    assert_called('GET', '/servers/1234/backup_schedule')    
    shell('backup-schedule sample-server --weekly monday')
    assert_called('POST', '/servers/1234/backup_schedule')

def test_backup_schedule_delete():
    shell('backup-schedule-delete 1234')
    assert_called('DELETE', '/servers/1234/backup_schedule')

def test_backup_schedule_boot():
    shell('boot --image 1 some-server')
    assert_called('POST', '/servers')

def test_flavors():
    shell('flavors')
    assert_called('GET', '/flavors/detail')
    
def test_images():
    shell('images')
    assert_called('GET', '/images/detail')