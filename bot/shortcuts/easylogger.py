"""
Copyright (c) 2022 dopebnan
"""

import time
import inspect

levels = {"": 0, "info": 10, "warn": 20, "error": 30, "critical": 40}


class Logger:
    def __init__(self, file, format, level=""):
        """The main class you need to set up before logging anything"""
        self.levels = levels
        self.level = level.lower()
        self.file = file
        self.format = format

    def log(self, level='', arg='', message='', cwfile=''):
        """logs the message"""
        cwfile = cwfile or inspect.stack()[1].filename.split('/')[-1]

        result = self.format
        if "$level" in result:
            result = result.replace("$level", level.upper())
        if "$message" in result:
            result = result.replace("$message", message)
        if "$time" in result:
            t = time.strftime("%b %d %H:%M:%S", time.localtime())
            result = result.replace("$time", t)
        if "$cwfile" in result:
            result = result.replace("$cwfile", cwfile)
        if "$arg" in result:
            result = result.replace("$arg", arg)

        if self.levels[level.lower()] >= self.levels[self.level.lower()]:
            print(result)
            with open(self.file, 'a') as f:
                f.write(result + '\n')

    def add_level(self, level_name, level: int):
        """To add another level to the logger"""
        self.levels[level_name.lower()] = level
        return self.levels
