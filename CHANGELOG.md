# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.2-Alpha] - 2017-09-22
### Added
- Emoji! Because emojis make the world look better
- Delete button function - clear your messages after you've read them so that you don't spam your chat up :)

### Changed

### Notes
- This will be the last update with new features until database restructuring is done
- Maintainence will take place from Sept 23 - Sept 24.
- The bot may go down and/or return errors over this period of time.
- All previously generated inline buttons / articles will no longer work.

## [0.3.1-Alpha] - 2017-09-19
### Added
- /new, /search and /rand commands.
- These commands work similarly to the existing functions, but are able to search across all existing sites

### Changed
- Updated rand command code.
- Fixed a small bug with the search commands.
- Cleaned up a little bit of code. I still need to do a major cleanup to remove redundant/repeated code.
- Restructured database
- Rewrote quite abit of code to work with the new database
- Rewrote scripts from [Matilda-tools](https://github.com/xlanor/matilda-tools) to work with the new database
- Wrote a migration script to move to the new structure.
- More changes to the database will take place - this is just the first stage to normalize the db.

### Notes
- today_new, today_search, today_rand is still not supported even though /new, /search, and /rand are able to search for today articles.
- This is because I still havent figured out how to update the db on the weekend.


## [0.3-Alpha] - 2017-09-18
### Added
- Support for TodayOnline (Weekday, Weekend)
- Some code for a new feature (search all)

### Changed
