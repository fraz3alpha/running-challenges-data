#!/bin/bash -e

git branch
# Make sure we are on the right branch
git checkout master

git config user.email "travis-data-auto-updater"
git config user.name "travis-data-auto-updater"
git add data/
git status

git add --all

git commit --message "Travis build: $TRAVIS_BUILD_NUMBER
- Triggered by ${TRAVIS_EVENT_TYPE}"
git log -1

if [ "${TRAVIS_BRANCH}" == "master" ]; then

    if [ "${GITHUB_TOKEN_RUNNING_CHALLENGES_DATA}" != "" ]; then

        git remote add origin-data https://${GITHUB_TOKEN_RUNNING_CHALLENGES_DATA}@github.com/fraz3alpha/running-challenges-data.git
        echo "Pushing commit to upstream"
        git push --quiet --set-upstream origin-data master
    else
        echo "Skipping push as GitHub token not available"
    fi
else
    echo "Skipping git commands as we aren't on master"
fi
