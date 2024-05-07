# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]
Check the [Amethyst](https://github.com/dopebnan/kwancore/blob/amethyst/changelog.md) changelog.

## [2.1]
### Changed
- Added kwanCore version into `sysinfo`

### Fixed
- `sysinfo` doesn't contain irrelevant pic info
- Code quality has been improving via linting
- `cogs.music` now accepts cookies to bypass age-restricted content
- Fixed `help`'s efficiency 
- Fixed `cogs.music` randomly disconnecting and stopping
- Made prefixed non-hardcoded
- Fixed `settings` not taking non-integer values

## [2.0] - 2022-09-24
### Changed
- Added compatibility for the new API changes

## [1.0.1] - 2022-07-04
### Added
- Load average into cpu_task logs
- Aliases for music commands

### Changed
- Moved `sysinfo` into `cogs.botinfo`
- Changed `is_pic` to `get_post_embed` in `cogs.memes`
  - instead of checking the headers, it just checks the post type and returns it as an embed

### Fixed
- temp_task looping upon getting triggered once
- Consistent case for logs
- FFmpeg option bugs
- Users being able to control the bot from a different voice channel

## [1.0] - 2022-05-01
