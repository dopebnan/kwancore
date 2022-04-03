"""
Copyright (c) 2022 dopebnan
"""

import time

class Logger:
    def __init__(self, file, format, cwf):
        self.file = file
        self.format = format
        self.cwf = cwf.split('/')[-1]

    def log(self, level='', arg='', message=''):
        """logs the message"""

        result = self.format
        if "$level" in result:
            result = result.replace("$level", level.upper())
        if "$message" in result:
            result = result.replace("$message", message)
        if "$time" in result:
            t = time.strftime("%b %d %H:%M:%S", time.localtime())
            result = result.replace("$time", t)
        if "$cwfile" in result:
            result = result.replace("$cwfile", self.cwf)
        if "$arg" in result:
            result = result.replace("$arg", arg)

        print(result)
        with open(self.file, 'a') as f:
            f.write(result + '\n')
