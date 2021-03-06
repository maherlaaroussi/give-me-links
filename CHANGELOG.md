# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]

## [0.7.4] - XX-05-2020

### Added

- Add the initialization interface when app is starting and getting data.

### Changed

- Correct the Makefile for a cleaning install & run.

### Fixed

- Fix the bug when trying to scrap a second time.

## [0.7.3] - 17-05-2020

### Added

- Properly quit the script.
- Succefully generate the right link with the language and quality chosen.

### Changed

- Correction of the algo to filter host.

## [0.7.2] - 16-05-2020

### Added

- Checking if the websie is alive before start doing anything.
- Check if the value of field pages is correct.

### Changed

- Qualities and languagesare now scrapped directly from website.
- Button start is now disabled until initialization are complete.

## [0.7.1] - 16-05-2020

### Changed

- Quality, language, host and pages can now be chosen by user.
- Button start are disabled when start scrapping.

## [0.7.0] - 2017-06-20

### Added

- PyQt5 is now used for graphical interface.
- Threads are used for scrapping to avoid window freeze.
- Configuration file.

## [0.6.0] - 14-05-2020

### Added

- Movies can be scrapped.
- UpToBox, 1fichier or both can be chosen.
- Quality of movies can be chosen.
- Languages of movies can be chosen.

[0.6.0]: https://gitlab.com/maherlaaroussi/give-me-links/-/releases#v0.6
[0.7.0]: https://gitlab.com/maherlaaroussi/give-me-links/-/tags/v0.7
[0.7.1]: https://gitlab.com/maherlaaroussi/give-me-links/-/tags/v0.7.1
[0.7.2]: https://gitlab.com/maherlaaroussi/give-me-links/-/tags/v0.7.2
[0.7.3]: https://gitlab.com/maherlaaroussi/give-me-links/-/tags/v0.7.3
[0.7.4]: https://gitlab.com/maherlaaroussi/give-me-links/-/tags/v0.7.4
[unreleased]: https://gitlab.com/maherlaaroussi/give-me-links/-/compare/v0.7...master
