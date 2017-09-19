# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
