The :program:`openstack-compute` shell utility
==============================================

.. program:: openstack-compute
.. highlight:: bash

The :program:`openstack-compute` shell utility interacts with OpenStack
Compute servers from the command line. It supports the entirety of the
OpenStack Compute API (plus a few Rackspace-specific additions), including
some commands not available from the Rackspace web console.

To try this out, you'll need a `Rackspace Cloud`__ account — or your own
install of OpenStack Compute (also known as Nova). If you're using Rackspace
you'll need to make sure to sign up for both Cloud Servers *and* Cloud Files
-- Rackspace won't let you get an API key unless you've got a Cloud Files
account, too. Once you've got an account, you'll find your API key in the
management console under "Your Account".

__ http://rackspacecloud.com/

You'll need to provide :program:`openstack-compute` with your Rackspace
username and API key. You can do this with the :option:`--username` and
:option:`--apikey` options, but it's easier to just set them as environment
variables by setting two environment variables:

.. envvar:: OPENSTACK_COMPUTE_USERNAME

    Your Rackspace Cloud username.

.. envvar:: OPENSTACK_COMPUTE_API_KEY

    Your API key.

For example, in Bash you'd use::

    export COPENSTACK_COMPUTE_USERNAME=yourname
    export COPENSTACK_COMPUTE_API_KEY=yadayadayada
    
From there, all shell commands take the form::
    
    openstack-compute <command> [arguments...]

Run :program:`openstack-compute help` to get a full list of all possible
commands, and run :program:`openstack-compute help <command>` to get detailed
help for that command.