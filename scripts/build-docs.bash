#!/bin/bash

pdoc --html --output-dir docs nextcloud_notes_api "$@"
mv -f ./docs/nextcloud_notes_api/* ./docs
rm -rf ./docs/nextcloud_notes_api