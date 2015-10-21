import os, sys, copy

from urllib import parse

import pyaml
import click

from vinegar import settings

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
    "pki_dir": "{path}/.vinegar/keys"
}

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
        print("Saltfile exists in {}, aborting".format(cwd))
        sys.exit(1)

    _make_saltfile(cwd)

    # Creating the vinegar directory
    if not os.path.exists(os.path.join(cwd, ".vinegar")):
        os.mkdir(os.path.join(cwd, ".vinegar"))

    if not os.path.exists(os.path.join(cwd, ".vinegar", "keys")):
        os.mkdir(os.path.join(cwd, ".vinegar", "keys"))

    if os.path.exists( os.path.join(cwd, "./vinegar", "master") ) and not force:
        print("master config exists in {}, aborting".format(cwd))

    _write_default_master(cwd)


@cli.command()
@click.argument("host")
@click.argument("name")
@click.option("--user", type=str)
@click.option("--password", type=str)
@click.option("--ssh-key", type=click.File())
def add(host, name, **kwargs):
    """adds a host to this salt-ssh environment"""
    cwd = os.getcwd()

    dct = {}
    _url = "ssh://{host}".format(host=host)
    url = parse.urlparse(_url)

    dct["host"] = url.hostname

    if not url.username and not kwargs.get("user", None):
        print("WARN: no username/implict username will be used")

    if url.username:
        dct["user"] = url.username
    elif kwargs.get("user", None):
        dct["user"] = kwargs["user"]

    if kwargs.get("priv", None):
        path = os.path.abspath(kwargs["priv"])
        if not os.path.exists(path):
            print("path %s does not exist".format(path))
            exit(1)
        dct["priv"] = path

    if kwargs.get("password", None):
        dct["passwd"] = kwargs["passwd"]

    output = os.path.join(cwd, ".vinegar", "roster")

    final = {}
    if os.path.exists(output):
        # read the file back in,
        with open(output) as fh:
            final = pyaml.load(fh.read())
    # set our name
    if final.get(name, None) is not None and not kwargs["force"]:
        print("remote {} already exists; maybe you meant `update`?".format(name))
        sys.exit(1)
    final[name] = dct
    # and write it out
    with open(output, "w+") as fh:
        fh.write( pyaml.dump(final, indent=4) )


def _make_saltfile(cwd):
    with open(os.path.join(cwd, "Saltfile"), "w") as fh:
        f = SALTFILE_DEFAULT.copy()
        f["salt-ssh"]["config_dir"] = f["salt-ssh"]["config_dir"].format(path=cwd)
        fh.write( pyaml.dump(f, indent=4) )

def _write_default_master(cwd):
    with open(os.path.join(cwd, ".vinegar/master"), "w") as fh:
        f = copy.deepcopy(MASTER_CONFIG_DEFAULT)
        f["file_roots"]["base"] = [path.format(path=cwd) for path in f["file_roots"]["base"]]
        f["pillar_roots"]["base"] = [path.format(path=cwd) for path in f["pillar_roots"]["base"]]
        f["pki_dir"] = f["pki_dir"].format(path=cwd)
