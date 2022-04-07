"""
Copyright (c) 2022 dopebnan
"""

import subprocess
import traceback
import time


def terminal(cmd):
    arg = cmd.split(' ')
    return subprocess.run(arg, stdout=subprocess.PIPE).stdout.decode('utf-8')


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

        if len(song) > 36:
            song = song[0:36]
            song += "…"
        else:
            song = song + ' ' * (37 - len(song))
        if index == i + 1:
            result += f"        You're here ↴\n"
        result += f" {i + 1}) {song} {length}      \n"

    result += "\n    You've hit the end of the queue\n```"
    return result


