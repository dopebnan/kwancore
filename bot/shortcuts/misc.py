"""
Copyright (c) 2022 dopebnan
"""
import subprocess
import traceback
import tempfile
import time


def terminal(cmd):
    """
    Runs your command in the terminal, and returns the output

    :param cmd:  str, the command
    :return:  str, the utf-8 decoded output from the terminal
    """
    with tempfile.TemporaryFile() as f:
        with subprocess.Popen(cmd, stdout=f, shell=True) as process:
            process.wait()
            f.seek(0)
            result = f.read()
    return result.decode("utf-8")


def save_traceback(error):
    """
    Save the traceback of an error to a file

    :param error:  error_obj, the error object
    :return:  int, the id of the file (i.e. the epoch timestamp of it)
    """
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
    """
    Format the music queue.

    :param queue:  dict, the music queue
    :param index:  int, the queue index
    :return:  str, the formatted queue
    """
    result = "```fsharp\n"
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
            result += "        You're here ↴\n"
        result += f" {i + 1}) {song} {length}      \n"

    result += "\n" + "You've hit the end of the queue!".center(42) + "\n```"

    if len(result) > 2000:
        num = (len(result) - 2000) + 1
        result = result[:-num] + "…"  # remove excess characters
        result = result[:-47]  # remove end queue line
        result += "\n" + "You've hit the end of the queue!".center(42) + "\n```"  # add back end queue line

    return result
