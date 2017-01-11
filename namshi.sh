#!/bin/bash

# Please run this script on your top level directory of all your git projects

# Enter Git token and user profile
AUTH_TOKEN=""
PROFILE=""
REPOS=`curl -i -H "Authorization: token "$AUTH_TOKEN"" https://api.github.com/users/$PROFILE/repos | grep ssh_url | cut -d"\"" -f4`

for repo in $REPOS; do
  git clone $repo
done

# List directories with VERSION.txt
DIR=$(find . -name VERSION.txt | cut -d'/' -f2)
echo $DIR
# Loop through all directories with VESION.txt
for i in $DIR; do
  cd $i && git pull
  git checkout -b version-hotfix
  # This sed command is for BSD, for linux use sed  -i 's/^N//' VERSION.txt
  sed -i '' 's/^N//' VERSION.txt
  cat VERSION.txt
  git add VERSION.txt
  git commit -m "Removed common preifx from version"
  git push origin version-hotfix
  # Please install pullr by running "npm install -g pullr"
  pullr -n -t "Refactoring VERSION.txt" -d "Removing common prefix from VERSION.txt"
  cd ..
done 
