#!/bin/bash

git branch

git config user.email "travis-data-auto-updater"
git config user.name "travis-data-auto-updater"
git add data/
git status
git commit --message "Travis build: $TRAVIS_BUILD_NUMBER\n\n  - Triggered by ${TRAVIS_EVENT_TYPE}"
git log -1

if [ "${GITHUB_TOKEN_RUNNING_CHALLENGES_DATA}" != "" ]; then 
    git remote add origin-data https://${GITHUB_TOKEN_RUNNING_CHALLENGES_DATA}@github.com/fraz3alpha/running-challenges-data.git
    git push --quiet --set-upstream origin-data test-data-branch
fi