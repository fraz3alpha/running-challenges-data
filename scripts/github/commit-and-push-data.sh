#!/bin/bash

git branch

git config user.email "travis-data-auto-updater"
git config user.name "travis-data-auto-updater"
git add data/
git status
git commit --message "Travis build: $TRAVIS_BUILD_NUMBER\n\n  - Triggered by ${TRAVIS_EVENT_TYPE}"
git log -1

if ["${TRAVIS_BRANCH}" == "master"]; then

    if [ "${GITHUB_TOKEN_RUNNING_CHALLENGES_DATA}" != "" ]; then

        git checkout -b master

        git remote add origin-data https://${GITHUB_TOKEN_RUNNING_CHALLENGES_DATA}@github.com/fraz3alpha/running-challenges-data.git
        git push --quiet --set-upstream origin-data master
    else
        echo "Skipping push as GitHub token not available"
    fi
else
    echo "Skipping git commands as we aren't on master"
fi