# KWANCORE

The kwancore project is an extensive "template" for python discord bots. 
You should modify it according to your desired results.

## Prerequisites
* [discord.py](https://github.com/Rapptz/discord.py)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [FFmpeg/FFprobe](https://git.ffmpeg.org/ffmpeg.git) 
* [AGenius.py](https://github.com/dopebnan/AGenius.py)

## Self-hosting
If you're here, you probably know how to host a discord bot already :)

## Notices

This template has been made for RaspberryPis, and has the highest possibility of NOT breaking on Raspbian. 
It will probably run fine on any Debian-based distro too, but I wouldn't recommend running this on Windows,
since some commands do require a bash terminal.

The whole entirety of this project is under [GNU General Public License v3](LICENSE),
except any libraries/modules that state otherwise (like the [shortcuts](bot/shortcuts) module, 
as it is under the [MIT License](bot/shortcuts/LICENSE)).

## Legal Notices

This project uses [discord.py](https://github.com/Rapptz/discord.py) by Rapptz as a Discord API wrapper, 
[yt-dlp](https://github.com/yt-dlp/yt-dlp) by yt-dlp as a way to get music from streaming services,
[FFmpeg/FFprobe](https://git.ffmpeg.org/ffmpeg.git) by the FFmpeg team to stream the media through the bot,
[AGenius.py](https://github.com/dopebnan/AGenius.py) by dopebnan, to load the lyrics of songs.

Also note that this project, despite using multiple libraries and/or modules, doesn't ship any of them with it. 
Any modules that this project uses belong to their respective owners, with their respective licenses.
If you wish to use this code, you must agree to those libraries'/modules' licenses.
