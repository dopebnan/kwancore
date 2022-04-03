"""
Copyright (c) 2022 dopebnan
"""

import subprocess


def terminal(cmd):
    arg = cmd.split(' ')
    return subprocess.run(arg, stdout=subprocess.PIPE).stdout.decode('utf-8')
