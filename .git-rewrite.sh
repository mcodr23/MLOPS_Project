#!/bin/sh

# Remove the backup from previous run if it exists
rm -rf .git/refs/original/

git filter-branch -f --env-filter '
OLD_EMAIL="64595758+Chandru-21@users.noreply.github.com"
CORRECT_NAME="mcodr23"
CORRECT_EMAIL="mancoder7@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --all
