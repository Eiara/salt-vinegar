import os, sys, copy
import six
from six.moves.urllib import parse

import pyaml
import click

from .. import settings

class FileNotFoundError(OSError): pass

SALTFILE_DEFAULT = {
    "salt-ssh": {
        "config_dir": "{path}/.vinegar"
    }
}

MASTER_CONFIG_DEFAULT = {
    "fileserver_backends":[
        "roots"
    ],
    "file_roots": {
        "base": [
            "{path}/srv/salt"
        ]
    },
    "pillar_roots": {
        "base": {
            "{path}/srv/pillar"
        }
    },
    "pki_dir": "{path}/.vinegar/keys",
    "ssh_log_dir": "{path}/.vinegar/logs/ssh.log"

}

def get_fn(filename):
    return os.path.join(os.getcwd(), settings.CONFIG_DIRECTORY, 
    filename)

def read_roster():
    """Read the rosterfile"""
    fn = get_fn("roster")
    if not os.path.exists(fn):
        raise FileNotFoundError("{} not found".format(fn))
        # read the file back in,
    roster = {}
    with open(fn) as fh:
        roster = pyaml.yaml.load(fh.read())
    if roster is None:
        roster = {}
    return roster

def write_roster(roster):
    fn = get_fn("roster")
    with open(fn,"w") as fh:
        fh.write(pyaml.dump(roster, indent=4))

# Create the click group to hold the cli command stuff

@click.group()
def cli():
    pass

@cli.command()
@click.option("--force/--no-force", default=False, help="forces output even when there's existing files")
def init(force):
    """Initialises salt-ssh in this directory"""

    cwd = os.getcwd()

    # creating the Saltfile
    if os.path.exists(os.path.join(cwd, "Saltfile")) and not force:
        sys.stderr.write("Saltfile exists in {}, aborting\n".format(cwd))
        sys.exit(1)

    _make_saltfile(cwd)

    # Creating the vinegar directory
    if not os.path.exists(os.path.join(cwd, ".vinegar")):
        os.makedirs(os.path.join(cwd, ".vinegar"))

    if not os.path.exists(os.path.join(cwd, ".vinegar", "keys")):
        os.makedirs(os.path.join(cwd, ".vinegar", "keys"))

    if os.path.exists( os.path.join(cwd, "./vinegar", "master") ) and not force:
        sys.stderr.write("master config exists in {}, aborting\n".format(cwd))

    _write_default_master(cwd)


@cli.command()
@click.argument("host")
@click.argument("name")
@click.option("--user", type=str)
@click.option("--password", type=str)
@click.option("--ssh-key", type=click.File())
def add(host, name, user=None, priv=None, **kwargs):
    """adds a host to this salt-ssh environment"""
    cwd = os.getcwd()

    dct = {}
    _url = "ssh://{host}".format(host=host)
    url = parse.urlparse(_url)

    dct["host"] = url.hostname

    if not url.username and not kwargs.get("user", None):
        sys.stderr.write("WARN: no username/implict username will be used\n")

    if url.username:
        dct["user"] = url.username
    elif kwargs.get("user", None):
        dct["user"] = kwargs["user"]

    if kwargs.get("priv", None):
        path = os.path.abspath(kwargs["priv"])
        if not os.path.exists(path):
            sys.stderr.write("path %(path)s does not exist".format(path))
            sys.exit(1)
        dct["priv"] = path

    if kwargs.get("password", None):
        dct["passwd"] = kwargs["password"]

    roster = read_roster()

    if roster.get(name, None) is not None and not kwargs["force"]:
        sys.stderr.write("remote {} already exists; maybe you meant `update`?".format(name))
        sys.exit(1)
    roster[name] = dct
    write_roster(roster)
    # and write it out

@cli.command()
@click.argument("name")
def rm(name):
    """
    Removes a named SSH target
    """
    roster = read_roster()
    if not name in roster:
        sys.stderr.write("{} not in roster")
        sys.exit(1)
    del roster[name]
    write_roster(roster)
    

@cli.command()
def list():
    roster = read_roster()
    for name, vals in roster.items():
        print("{name}:".format(name=name))
        print("\t {user}@{host}".format(**vals))
        if vals.get("passwd"):
            print("\t password auth")
        elif vals.get("ssh-priv"):
            print("\t key auth")
        else:
            print("\t no auth")

def _make_saltfile(cwd):
    with open(os.path.join(cwd, "Saltfile"), "w") as fh:
        copied = copy.deepcopy(SALTFILE_DEFAULT)
        copied["salt-ssh"]["config_dir"] = copied["salt-ssh"]["config_dir"].format(path=cwd)
        fh.write( pyaml.dump(copied, indent=4) )

def _write_default_master(cwd):
    with open(os.path.join(cwd, ".vinegar/master"), "w") as fh:
        copied = copy.deepcopy(MASTER_CONFIG_DEFAULT)
        copied["file_roots"]["base"] = [path.format(path=cwd) for path in copied["file_roots"]["base"]]
        copied["pillar_roots"]["base"] = [path.format(path=cwd) for path in copied["pillar_roots"]["base"]]
        copied["pki_dir"] = copied["pki_dir"].format(path=cwd)
        fh.write( pyaml.dump(copied, indent=4) )
