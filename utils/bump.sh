#!/bin/bash

# Init UI colors
NC="\033[0m"    # no color
BR="\033[1;91m" # bright red
BY="\033[1;33m" # bright yellow
BG="\033[1;92m" # bright green
BW="\033[1;97m" # bright white

# Init manifest path
manifest="chromium/extension/manifest.json"

# Bump version
echo -e "${BY}\nBumping version in ${manifest}...${NC}\n"
today=$(date +'%Y.%-m.%-d') # YYYY.M.D format
new_versions=() # for dynamic commit msg
old_ver=$(sed -n 's/.*"version": *"\([0-9.]*\)".*/\1/p' "$manifest")
if [[ $old_ver == "$today" ]]  # exact match for $today
    then # bump to $today.1
        NEW_VER="$today.1"
elif [[ $old_ver == "$today."* ]] # partial match for $today
    then # bump to $today.n+1
        last_number=$(echo "$old_ver" | awk -F '.' '{print $NF}')
        NEW_VER="$today.$((last_number + 1))"
else # no match for $today
    # bump to $today
        NEW_VER="$today"
fi
sed -i "s/\"version\": \"$old_ver\"/\"version\": \"$NEW_VER\"/" "$manifest"
echo -e "${BW}v${old_ver}${NC} → ${BG}v${NEW_VER}${NC}"

# Commit/push bump(s)
echo -e "${BY}\nCommitting bump to Git...\n${NC}"
git add ./**/manifest.json
git commit -n -m "Bumped \`version\` to $NEW_VER"
git push

# Print final summary
echo -e "\n${BG}Success! ${manifest} updated/committed/pushed to GitHub${NC}"
