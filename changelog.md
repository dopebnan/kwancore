# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [Unreleased]
### Added
- **cogs/money**: you can build an economy with this cog
  - **money_start**: this command adds you to the money database
  - **profile**: this command will display your profile and stats
  - **inventory**: displays your inventory
  - **item**: searches for an item in the database and displays info about it
- **errors.MoneyError**: base error for errors involving the money stuff
  - **ProfileAlreadyExists**: gets raised when the profile you're trying to add to the database is already present there
  - **ProfileNotFound**: gets raised when a profile isn't present in the database
  - **ItemNotFound**: get raised when an item isn't present in the database

### Changed
- **shortcuts**: added proper documentation
- made the command brief's better
