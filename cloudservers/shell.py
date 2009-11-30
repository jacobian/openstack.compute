import os
import argparse

def main():
    parser = argparse.ArgumentParser("Command-line access to the Rackspace Cloud Servers API")
    parser.add_argument("--username", default=env('CLOUDSERVERS_USERNAME'), "API username")
    parser.add_argument("--api-key", default=env('CLOUDSERVERS_API_KEY'), "API key")
    
    subparsers = parser.add_subparsers(title="subcommands")
    
    p = subparsers.add_parser('flavors', help="List available flavors")
    p.set_defaults(func=list_flavors)
    
    p = subparsers.add_parser('servers', help='List current servers')
    p.set_defaults(func=list_servers)
    
    options, args = parser.parse_args()
    args.func(options, args)

def env(name):
    return os.environ.get(name, '')
    
def list_flavors(options, args):
    print "list flavors"
    
def list_servers(options, args):
    print "list servers"