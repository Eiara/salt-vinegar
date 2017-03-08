TREE_DEFAULT = {
    "srv": {
        "salt": {
            "__files__": [
                "top.sls",
                "base.sls"
            ]
        },
        "pillar": {
            "__files__": [
                "top.sls",
                "base.sls"
            ]
        }
        
    }
}

import pyaml
import click

