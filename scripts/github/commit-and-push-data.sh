#!/bin/bash

git config --global user.email "travis-data-auto-updater"
git config --global user.name "travis-data-auto-updater"
git add data/
git status
git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
