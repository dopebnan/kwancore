<div align="center">

[![kwanCore](https://raw.githubusercontent.com/dopebnan/kwancore/main/assets/logo.png)](README.md "[kwanCore]")

[![Latest Release](https://img.shields.io/github/v/release/dopebnan/kwancore?display_name=release&sort=semver)](https://github.com/dopebnan/kwancore/releases)
[![GitHub Workflow](https://img.shields.io/github/workflow/status/dopebnan/kwancore/Linting)](https://github.com/dopebnan/kwancore/actions/workflows/linting.yml)
[![discord.py](https://img.shields.io/badge/-discord.py-5865F2)](https://github.com/Rapptz/discord.py)
[![License: GPLv3](https://img.shields.io/github/license/dopebnan/kwancore)](LICENSE)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/dopebnan/kwancore)](https://github.com/dopebnan/kwancore/commits)
![Last Commit](https://img.shields.io/github/last-commit/dopebnan/kwancore)

kwanCore is a discord.py bot foundation. Everything is set up for you, you just need to tweak some settings
for your liking.
</div>


## Prerequisites
* [discord.py](https://github.com/Rapptz/discord.py)
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* [FFmpeg/FFprobe](https://git.ffmpeg.org/ffmpeg.git) 
* [AGenius.py](https://github.com/dopebnan/AGenius.py)
* [Async PRAW](https://github.com/praw-dev/asyncpraw)
* [PyYAML](https://github.com/yaml/pyyaml)

## Self-hosting
You need to create a file named `config.yaml` inside `bot/usercontent/`.
That file's contents have to look something like this:
```yaml
warningChannel:  # The snowflake ID of the discord channel where the warnings would be sent to
token:  # Your bot's discord token
genius_token:  # A Genius.com token for lyrics (https://genius.com/api-clients/new)

reddit:  # Here are the Reddit configs (https://www.reddit.com/prefs/apps/)
  client_id:  # 14-character string under "personal use script"
  client_secret:  # 27-character string under "secret"
  password:  # The password for the Reddit account used for said application 
  user_agent:  # The user-agent for the application (should follow this format: <platform>:<app ID>:<version string> (by /u/<reddit username>))
  username:  # The username of the Reddit accound used for said application

dev_role:  # NAME of the developer role used to access the dev cog

default_settings:  # Default settings
  pic_cooldown:  # cooldown between pic commands IN SECONDS
  pic_cooldown_bool:  # If it should display a cooldown message for pic commands
  echo_cooldown:  # cooldown between echo commands IN SECONDS
```

Then you just need to start the bot by running `bot/main.py` in a terminal.
It will create some files it needs, and then you're good to go!

## Notices

This template has been made for RaspberryPis, and has the highest possibility of NOT breaking on Raspbian. 
It will probably run fine on any Debian-based distro too, but I wouldn't recommend running this on Windows,
since some commands do require bash (i.e. checking the system uptime).

## Legal Notices

The whole entirety of this project is under the [GNU General Public License v3](LICENSE),
except any files that state otherwise.

This project requires that your machine has some prerequisites installed:
[discord.py](https://github.com/Rapptz/discord.py) by Rapptz as a Discord API wrapper, 
[yt-dlp](https://github.com/yt-dlp/yt-dlp) by yt-dlp as a way to get music from streaming services,
[FFmpeg/FFprobe](https://git.ffmpeg.org/ffmpeg.git) by the FFmpeg team to stream the media through the bot,
[AGenius.py](https://github.com/dopebnan/AGenius.py) by dopebnan, to load the lyrics of songs,
[Async PRAW](https://github.com/praw-dev/asyncpraw) by praw-dev, to access reddit via python,
[PyYAML](https://github.com/yaml/pyyaml) by YAML, to load `.yaml` files.

Also note that this project, despite using multiple libraries and/or modules, doesn't ship any of them with it. 
Any modules that this project uses belong to their respective owners, with their respective licenses.
If you wish to use this code, you must agree to those libraries'/modules' licenses.
