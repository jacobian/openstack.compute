import os
import sys
import cmdln
import cloudservers
import httplib2
import prettytable

class CloudServersShell(cmdln.Cmdln):
    """Usage:
        cloudservers [opts] SUBCOMMAND [opts]
        cloudservers help SUBCOMMAND
        
    ${option_list}
    ${command_list}
    """
    name = 'cloudservers'
    version = cloudservers.__version__
    
    def get_optparser(self):
        parser = cmdln.Cmdln.get_optparser(self)
        parser.add_option('--http-debug', dest='debug', default=False, action='store_true')
        parser.add_option('--username', default=env('CLOUD_SERVERS_USERNAME'),
                          help='Defaults to env[CLOUD_SERVERS_USERNAME]')
        parser.add_option('--apikey', default=env('CLOUD_SERVERS_API_KEY'),
                          help='Defaults to env[CLOUD_SERVERS_API_KEY]')
        return parser
        
    def postoptparse(self):
        user, apikey = self.options.username, self.options.apikey
        if not user:
            raise cmdln.CmdlnError("You must provide a username, either via "
                                   "--username or via env[CLOUD_SERVERS_USERNAME]")
        if not apikey:
            raise cmdln.CmdlnError("You must provide an API key, either via "
                                   "--apikey or via env[CLOUD_SERVERS_API_KEY]")

        if self.options.debug:
            httplib2.debuglevel = 10

        self.cs = cloudservers.CloudServers(user, apikey)
        try:
            self.cs.authenticate()
        except cloudservers.Unauthorized:
            raise cmdlin.CmdlnError("Invalid Cloud Servers credentials.")
    
    def do_flavors(self, subcmd, opts):
        """Print a list of available 'flavors' (sizes of servers).
        
        Usage:
            cloudservers flavors
        """
        self._print_list(self.cs.flavors.list(), ['ID', 'Name', 'RAM', 'Disk'])

    def do_images(self, subcmd, opts):
        """Print a list of available images to boot from.
        
        Usage:
            cloudservers images
        """
        self._print_list(self.cs.images.list(), ['ID', 'Name', 'Status'])

    def do_list(self, subcmd, opts):
        """List active cloud servers.
        
        Usage:
            cloudservers list
        """
        self._print_list(self.cs.servers.list(), ['ID', 'Name', 'Status'])

    @cmdln.option('-f', '--flavor', default=None, help="Flavor ID (see 'cloudservers flavors'). Defaults to 256MB RAM instance.")
    @cmdln.option('-i', '--image', default=None, help="Image ID (see 'cloudservers images'). Defaults to Ubuntu 9.10.")
    @cmdln.option('-I', '--ipgroup', default=None, help="IP group ID (see 'cloudservers ipgroups').")
    @cmdln.option('-m', '--meta', metavar="KEY=VALUE", action="append", help="Record arbitrary key/value metadata.")
    def do_boot(self, subcmd, opts, name):
        """Start a new server.
        
        Usage:
            cloudservers boot [options] NAME
        
        ${cmd_option_list}
        """
        flavor = opts.flavor or self._get_default_flavor()
        image = opts.image or self._get_default_image()
        if opts.meta:
            metadata = dict(v.split('=') for v in opts.meta)
        else:
            metadata = None
        server = self.cs.servers.create(name, image, flavor, opts.ipgroup, metadata)
        print "Booting server ID %s." % server.id

    def do_show(self, subcmd, opts, server_id):
        """Show details about the given server.
        
        Usage:
            cloudservers show SERVER_ID
        """
        s = self.cs.servers.get(int(server_id))
        self._print_dict(s._info)
    
    # TODO: --force option, prompt otherwise
    def do_delete(self, subcmd, opts, server_id):
        """Immediately shut down and delete a server.
        
        Usage:
            cloudservers delete [options] SERVER_ID
        """
        self.cs.servers.delete(int(server_id))
        print "OK."
    
    def _get_default_flavor(self):
        for fl in self.cs.flavors.list():
            if fl.ram == 256:
                return fl

    def _get_default_image(self):
        for im in self.cs.images.list():
            if im.name.startswith('Ubuntu 9.10'):
                return im

    def _print_list(self, objs, fields):
        pt = prettytable.PrettyTable([f for f in fields], caching=False)
        pt.aligns = ['l' for f in fields]
        for o in objs:
            pt.add_row([getattr(o, f.lower().replace(' ', ''), '') for f in fields])
        pt.printt(sortby=fields[0])
        
    def _print_dict(self, d):
        pt = prettytable.PrettyTable(['Property', 'Value'], caching=False)
        pt.aligns = ['l', 'l']
        [pt.add_row(list(r)) for r in d.iteritems()]
        pt.printt(sortby='Property')

def env(name):
    return os.environ.get(name, '')

def main():
    sys.exit(CloudServersShell().main())