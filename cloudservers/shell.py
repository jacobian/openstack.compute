"""
Command-line interface to the Cloud Servers API.
"""

import argparse
import cloudservers
import httplib2
import os
import prettytable
import sys
import textwrap

# Choices for flags.
DAY_CHOICES = [getattr(cloudservers, i) for i in dir(cloudservers) if i.startswith('BACKUP_WEEKLY_')]
HOUR_CHOICES = [getattr(cloudservers, i) for i in dir(cloudservers) if i.startswith('BACKUP_DAILY_')]

def pretty_choice_list(l): return ', '.join("'%s'" % i for i in l)

# Decorator for args
def arg(*args, **kwargs):
    def _decorator(func):
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.__dict__.setdefault('arguments', []).insert(0, (args, kwargs))
        return func
    return _decorator

class CommandError(Exception):
    pass

class CloudserversShell(object):
    def main(self, argv):
        self.parser = argparse.ArgumentParser(
            prog = 'cloudservers',
            description = __doc__.strip(),
            epilog = 'See "cloudservers help COMMAND" for help on a specific command.',
            add_help = False,
            formatter_class = CloudserversHelpFormatter,
        )
        
        # Global arguments
        env = lambda n: os.environ.get(n, '')
        
        self.parser.add_argument('-h', '--help',
            action = 'help',
            help = argparse.SUPPRESS,
        )
        
        self.parser.add_argument('--debug', 
            default = False, 
            action = 'store_true',
            help = argparse.SUPPRESS)
            
        self.parser.add_argument('--username',
            default = env('CLOUD_SERVERS_USERNAME'),
            help = 'Defaults to env[CLOUD_SERVERS_USERNAME].')
            
        self.parser.add_argument('--apikey',
            default = env('CLOUD_SERVERS_API_KEY'),
            help='Defaults to env[CLOUD_SERVERS_API_KEY].')
        
        # Subcommands
        subparsers = self.parser.add_subparsers(metavar='<subcommand>')
        self.subcommands = {}
        
        # Everything that's do_* is a subcommand.
        for attr in (a for a in dir(self) if a.startswith('do_')):
            # I prefer to be hypen-separated instead of underscores.
            command = attr[3:].replace('_', '-')
            callback = getattr(self, attr)
            desc = callback.__doc__ or ''
            help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])
            
            subparser = subparsers.add_parser(command, 
                help = help,
                description = desc,
                add_help=False,
                formatter_class = CloudserversHelpFormatter
            )
            subparser.add_argument('-h', '--help',
                action = 'help',
                help = argparse.SUPPRESS,
            )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)
                
        # Parse args and call whatever callback was selected
        args = self.parser.parse_args(argv)
                
        # Deal with global arguments
        if args.debug:
            httplib2.debuglevel = 1
           
        user, apikey = args.username, args.apikey
        if not user:
            raise CommandError("You must provide a username, either via "
                               "--username or via env[CLOUD_SERVERS_USERNAME]")
        if not apikey:
            raise CommandError("You must provide an API key, either via "
                               "--apikey or via env[CLOUD_SERVERS_API_KEY]")

        self.cs = cloudservers.CloudServers(user, apikey)
        try:
            self.cs.authenticate()
        except cloudservers.Unauthorized:
            raise CommandError("Invalid Cloud Servers credentials.")
        
        args.func(args)
        
    @arg('command', metavar='<subcommand>', nargs='?', help='Display help for <subcommand>')
    def do_help(self, args):
        """
        Display help about this program or one of its subcommands.
        """
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise CommandError("'%s' is not a valid subcommand." % args.command)
        else:
            self.parser.print_help()
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    @arg('--enable', dest='enabled', action='store_true', help='Enable backups.')
    @arg('--disable', dest='enabled', action='store_false', help='Disable backups.')
    @arg('--weekly', metavar='<day>', choices=DAY_CHOICES,
         help='Schedule a weekly backup for <day> (one of: %s).' % pretty_choice_list(DAY_CHOICES))
    @arg('--daily', metavar='<time-window>', choices=HOUR_CHOICES,
         help='Schedule a daily backup during <time-window> (one of: %s).' % pretty_choice_list(HOUR_CHOICES))
    def do_backup_schedule(self, args):
        """
        Show or edit the backup schedule for a server.
        
        With no flags, the backup schedule will be shown. If flags are given,
        the backup schedule will be modified accordingly.
        """
        pass
        
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_backup_schedule_delete(self, args):
        """
        Delete the backup schedule for a server.
        """
        pass
    
    @arg('--flavor',
         default = None, 
         metavar = '<flavor>',
         help = "Flavor ID (see 'cloudservers flavors'). Defaults to 256MB RAM instance.")
    @arg('--image', 
         default = None,
         metavar = '<image>',
         help = "Image ID (see 'cloudservers images'). Defaults to Ubuntu 9.10.")
    @arg('--ipgroup',
         default = None, 
         metavar = '<group>',
         help = "IP group ID (see 'cloudservers ipgroups').")
    @arg('--meta', 
         metavar = "key=value", 
         nargs = '*',
         help = "Record arbitrary key/value metadata.")
    @arg('name', metavar='<name>', help='Name for the new server')
    def do_boot(self, args):
        """Boot a new server."""
        flavor = args.flavor or self.cs.flavors.find(ram=256)
        image = args.image or self.cs.images.find(name="Ubuntu 9.10 (karmic)")
        if args.meta:
            metadata = dict(v.split('=') for v in args.meta)
        else:
            metadata = None
        server = self.cs.servers.create(args.name, image, flavor, args.ipgroup, metadata)
        print "Booting server ID %s." % server.id
    
    def do_flavors(self, args):
        """Print a list of available 'flavors' (sizes of servers)."""
        print_list(self.cs.flavors.list(), ['ID', 'Name', 'RAM', 'Disk'])
    
    def do_images(self, args):
        """Print a list of available images to boot from."""
        print_list(self.cs.images.list(), ['ID', 'Name', 'Status'])

    @arg('server', metavar='<server>', help='Name or ID of server.')
    @arg('group', metavar='<group>', help='Name or ID of group.')
    @arg('address', metavar='<address>', help='IP address to share.')
    def do_ip_share(self, args):
        """Share an IP address from the given IP group onto a server."""
        pass
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    @arg('address', metavar='<address>', help='IP address to share.')
    def do_ip_unshare(self, args):
        """Stop sharing the given address."""
        pass

    def do_ipgroup_list(self, args):
        """Show IP groups."""
        print_list(self.cs.ipgroups.list(), ['ID', 'Name', 'Servers'])
        
    @arg('group', metavar='<group>', help='Name or ID of group.')
    def do_ipgroup_show(self, args):
        """Show details about a particular IP group."""
        pass
    
    @arg('name', metavar='<name>', help='What to name this new group.')
    @arg('server', metavar='<server>', nargs='?',
         help='Server (name or ID) to make a member of this new group.')
    def do_ipgroup_create(self, args):
        """Create a new IP group."""
        pass
        
    @arg('group', metavar='<group>', help='Name or ID of group.')
    def do_ipgroup_delete(self, args):
        """Delete an IP group."""
        pass
    
    def do_list(self, args):
        """List active servers."""
        print_list(self.cs.servers.list(), ['ID', 'Name', 'Status'])
    
    @arg('--hard',
        dest = 'reboot_type',
        action = 'store_const',
        const = cloudservers.REBOOT_HARD,
        default = cloudservers.REBOOT_SOFT,
        help = 'Perform a hard reboot (instead of a soft one).')
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_reboot(self, args):
        """Reboot a server."""
        server = self._find_server(args.server)
        server.reboot(args.reboot_type)
        print "Rebooting server ID %s." % server.id
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    @arg('image', metavar='<image>', help="Name or ID of new image.")
    def do_rebuild(self, args):
        """Shutdown, re-image, and re-boot a server."""
        pass
        
    @arg('server', metavar='<server>', help='Name (old name) or ID of server.')
    @arg('name', metavar='<name>', help='New name for the server.')
    def do_rename(self, args):
        """Rename a server."""
        pass
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    @arg('flavor', metavar='<flavor>', help = "Name or ID of new flavor.")
    def do_resize(self, args):
        """Resize a server."""
        pass
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_resize_confirm(self, args):
        """Confirm a previous resize."""
        pass
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_resize_revert(self, args):
        """Revert a previous resize (and return to the previous VM)."""
        pass
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_root_password(self, args):
        """
        Change the root password for a server.
        """
        pass
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_show(self, args):
        """Show details about the given server."""
        s = self.cs.servers.get(self._find_server(args.server))
        print_dict(s._info)
    
    @arg('server', metavar='<server>', help='Name or ID of server.')
    def do_delete(self, args):
        """Immediately shut down and delete a server."""
        self.cs.servers.delete(self._find_server(args.server))
        print "OK."
        
    def _find_server(self, server):
        """Get a server by name or ID."""
        try:
            if server.isdigit():
                return self.cs.servers.get(int(server))
            else:
                return self.cs.servers.find(name=server)
        except cloudservers.NotFound:
            raise CommandError("No server with a name or ID of '%s'." % server)

# I'm picky about my shell help.
class CloudserversHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(CloudserversHelpFormatter, self).start_section(heading)

# Helpers
def print_list(objs, fields):
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.aligns = ['l' for f in fields]
    for o in objs:
        pt.add_row([getattr(o, f.lower().replace(' ', ''), '') for f in fields])
    pt.printt(sortby=fields[0])
    
def print_dict(d):
    pt = prettytable.PrettyTable(['Property', 'Value'], caching=False)
    pt.aligns = ['l', 'l']
    [pt.add_row(list(r)) for r in d.iteritems()]
    pt.printt(sortby='Property')

def main():
    try:
        CloudserversShell().main(sys.argv[1:])
    except CommandError, e:
        print >> sys.stderr, e
        sys.exit(1)