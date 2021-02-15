# nextcloud-notes-api

<a
  href="https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ATest"
  target="_blank" style="float: left; margin-right: 1rem;">
<img src="https://github.com/coma64/nextcloud-notes-api/workflows/Test/badge.svg"
    alt="Test" style="display: inline;">
</a>

<a
  href="https://github.com/coma64/nextcloud-notes-api/actions?query=workflow%3ASuper-Linter"
  target="_blank" style="float: left; margin-right:1rem;">
<img src="https://github.com/coma64/nextcloud-notes-api/workflows/Super-Linter/badge.svg"
    alt="Test" style="display: inline;">
</a>

<a href="https://codecov.io/gh/coma64/nextcloud-notes-api" target="_blank">
<img
src="https://img.shields.io/codecov/c/github/coma64/nextcloud-notes-api?color=%2334D058"
alt="Coverage" style="display: inline;">
</a>
<br />

## About

A [Nextcloud Notes](https://github.com/nextcloud/notes) API wrapper

## Todo

- [x] fix typehints
- [x] store datetime object instead of float in Note.modified
- [x] add license
- [x] remove Note.from_dict and use init with keyword args instead
- [x] add NotesApi docs
- [ ] update Note tests
- [x] use generic type hints (List -> Sequence)
- [ ] publish to pip and readthedocs
- [x] stricter code formatter than autopep8
- [x] run tests powershell / shell script
- [x] build docs shell script
- [ ] usage examples
- [x] classes
  - [x] NotesApi
    - [x] api endpoints
