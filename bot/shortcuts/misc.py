"""
Copyright (c) 2022 dopebnan
"""
import os
import subprocess
import traceback
import tempfile
import time


def terminal(cmd):
    with tempfile.TemporaryFile() as f:
        process = subprocess.Popen(cmd, stdout=f, shell=True)
        process.wait()
        f.seek(0)
        result = f.read()
    return result


def save_traceback(error):
    result = ""
    e = traceback.format_exception(None, error, error.__traceback__)
    e.pop(0)  # remove first line
    for ln in e:
        if ln.startswith('\n'):  # don't open second discord traceback
            break
        result += ln
    err_id = int(time.time())
    with open(f"traceback/{err_id}", 'w') as f:
        f.write(result)

    return err_id


def queue_format(queue, index):
    result = f"```fsharp\n"
    for i in range(0, len(queue)):
        song = queue[i][0]['title'] + ' — ' + queue[i][0]['artist']
        length = queue[i][0]['length']
        duration = str(length % 60)
        if len(duration) < 2:
            duration = '0' + duration
        length = str(length // 60) + ':' + duration

        if len(song) > 32:
            song = song[0:32]
            song += "…"
        else:
            song = song + ' ' * (32 - len(song))
        if index == i + 1:
            result += f"        You're here ↴\n"
        result += f" {i + 1}) {song} {length}      \n"

    result += "\n" + "You've hit the end of the queue!".center(42) + "\n```"

    if len(result) > 2000:
        num = (len(result) - 2000) + 1
        result = result[:-num] + "…"  # remove excess characters
        result = result[:-47]  # remove end queue line
        result += "\n" + "You've hit the end of the queue!".center(42) + "\n```"  # add back end queue line

    return result


