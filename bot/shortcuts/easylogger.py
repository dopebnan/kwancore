"""
Copyright (c) 2022 dopebnan
"""

import time
import inspect

levels = {"": 0, "info": 10, "warn": 20, "error": 30, "critical": 40}


class Logger:
    def __init__(self, file, format_, level=""):
        """
        Main logger.

        You need to set this up once per logger instance.

        format_ variables:
            $level:  the log level;
            $message:  the actual message;
            $time:  the time in ISO-8601 format;
            $cwfile:  current working file, i.e. the file which the log came from;
            $arg:  and extra argument;

        :param file:  str, path to the file which will contain the logs
        :param format_: str, a string in the format you'd like your logs in;
        :param level: str, which level to log at.

        """
        self.levels = levels
        self.level = level.lower()
        self.file = file
        self.format = format_

    def log(self, level='', arg='', message='', cwfile=''):
        """
        Logs your message.

        :param level:  str, level of the log
        :param arg:  str, replaces '$arg' in the log string
        :param message:  str, the message
        :param cwfile:  str, replaces '$cwfile'
        """
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
        """
        Add another level to the log.

        Default levels:
        {"": 0, "info": 10, "warn": 20, "error": 30, "critical": 40}

        :param level_name:  str, the name of the level
        :param level:  int, value of the level
        :return:  dict, dictionary with the levels and values
        """
        self.levels[level_name.lower()] = level
        return self.levels
