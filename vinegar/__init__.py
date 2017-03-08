from ._version import __version__

from .commands import base
from .commands.subcommands import ssh

class Commands(click.MultiCommand):
    
    def __init__(self, *args, **kwargs):
        self.__subs = {
            ssh.command: ssh.cli
        }
    def list_commands(self, ctx):
        return self.__subs.keys()
        
    def get_command(self, ctx, name):
        return self.__subs[name]

def init():
    cli = Commands(help="vinegar {}".format(__version__))
    cli()