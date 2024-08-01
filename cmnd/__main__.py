# This file is placed in the Public Domain.
# pylint: disable=C0413,W0105,W0212,W0613,E0401


"runtime"


import base64
import getpass
import os
import sys
import time


from .cfg    import Config
from .cmds   import Commands
from .dft    import Default
from .errors import errors
from .disk   import Persist, find, last, skel, sync
from .main   import cmnd, enable
from .object import construct, edit, fmt, keys, update
from .parse  import parse
from .run    import fleet
from .utils  import fntime, laps, privileges


"config"


Cfg         = Config()
Cfg.name    = "cmnd"
Cfg.user    = getpass.getuser()
Cfg.wdr     = os.path.expanduser(f"~/.{Cfg.name}")
Cfg.pidfile = os.path.join(Cfg.wdr, f"{Cfg.name}.pid")


Persist.workdir = Cfg.wdr


def cmd(event):
    "list commands."
    event.reply(",".join(sorted(keys(Commands.cmds))))


"runtime"


def skl(event):
    "create service file (pipx)."
    privileges(getpass.getuser())
    skel()


def srv(event):
    "create service file (pipx)."
    if event.args:
        username = event.args[0]
    else:
        username  = getpass.getuser()
    txt = f"""[Unit]
Description={Cfg.name.upper()}
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
User={username}
Group={username}
ExecStartPre=/home/{username}/.local/bin/{Cfg.name} skl
ExecStart=/home/{username}/.local/bin/{Cfg.name}d
ExitType=cgroup
KillSignal=SIGKILL
KillMode=control-group
RemainAfterExit=yes
Restart=no

[Install]
WantedBy=default.target"""
    event.reply(txt)


def main():
    "main"
    parse(Cfg, " ".join(sys.argv[1:]))
    enable(print)
    from cmnd import __main__
    Commands.scan(__main__)
    cmnd(Cfg.otxt, print)


"main"


if __name__ == "__main__":
    main()
    errors()
