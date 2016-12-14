# salt-vinegar

## What

`salt-vinegar` is a tool in the line of `knife` for Chef, intended to make it
somewhat easier to manage the development and maintenance of a SaltStack repository and `salt-ssh`-based
infrastructure.

Currently only two functions are supported: initialising a localised `salt-ssh` directory and adding hosts.

## Usage

`vinegar ssh init`

 - Creates a Saltfile and a `.vinegar` directory, with a `master` configuration set to the current working directory.

`vinegar ssh add <user>@<host> <name> --password <password>`

  - Adds an SSH host w/ username & password that can be managed with `salt-ssh`.

`vinegar ssh add <user>@<host> <name> --priv /path/to/private/key>`
  - Uses a SSH private key instead of password auth.

## TODO

`vinegar init [--path]`

Create a new Saltstack repo in the specified path

`vinegar ssh rm <user>@<host> <name>`

Remove a host from salt-ssh