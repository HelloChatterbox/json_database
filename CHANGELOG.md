# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

current dev branch

### Added

- length property for db ( len(db) == number of items )
- InvalidItemID and DatabaseNotCommitted exceptions

### Changed

- remove get_key method from JsonDatabase
- support accessing db by item_id ( item = db[item_id] )
- support assigning item by item_id ( db[item_id] = item )

### Fixed

- support arbitrary objects in JsonDatabase
    - get_item_id
    - update_item

## [0.1.0]

initial release


[unreleased]: https://github.com/OpenJarbas/json_database/tree/dev
[0.1.0]: https://github.com/OpenJarbas/json_database/tree/0.1.0
