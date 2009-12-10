from __future__ import absolute_import

import os
from cloudservers.shell import CloudserversShell
from .fakeserver import FakeServer

# Patch os.environ to avoid required auth info.
def setup():
    global _old_env
    fake_env = {
        'CLOUD_SERVERS_USERNAME': 'username',
        'CLOUD_SERVERS_API_KEY': 'password'
    }
    _old_env, os.environ = os.environ, fake_env

def teardown():
    global _old_env
    os.environ = _old_env

# Make a fake shell object, a helping wrapper to call it, and a quick way
# of asserting that certain API calls were made.
_shell = CloudserversShell()
_shell._api_class = FakeServer
assert_called = lambda m, u: _shell.cs.assert_called(m, u)
shell = lambda cmd: _shell.main(cmd.split())

"""
backup-schedule     Show or edit the backup schedule for a server.
backup-schedule-delete
                    Delete the backup schedule for a server.
boot                Boot a new server.
delete              Immediately shut down and delete a server.
flavors             Print a list of available 'flavors' (sizes of
                    servers).
help                Display help about this program or one of its
                    subcommands.
images              Print a list of available images to boot from.
ip-share            Share an IP address from the given IP group onto a
                    server.
ip-unshare          Stop sharing the given address.
ipgroup-create      Create a new IP group.
ipgroup-delete      Delete an IP group.
ipgroup-list        Show IP groups.
ipgroup-show        Show details about a particular IP group.
list                List active servers.
reboot              Reboot a server.
rebuild             Shutdown, re-image, and re-boot a server.
rename              Rename a server.
resize              Resize a server.
resize-confirm      Confirm a previous resize.
resize-revert       Revert a previous resize (and return to the previous
                    VM).
root-password       Change the root password for a server.
show                Show details about the given server.
"""

def test_flavors():
    shell('flavors')
    assert_called('GET', '/flavors/detail')