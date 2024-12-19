#!/bin/bash

# Bumps Chromium manifest if changes detected + git commit/push

shopt -s nocasematch # enable case-insensitive matching (to flexibly check commit msg for bumps)

# Init UI COLORS
NC="\033[0m"    # no color
BR="\033[1;91m" # bright red
BY="\033[1;33m" # bright yellow
BG="\033[1;92m" # bright green
BW="\033[1;97m" # bright white

# Init manifest PATH
MANIFEST_PATH="chromium/extension/manifest.json"

echo -e "${BY}\nBumping version in ${MANIFEST_PATH}...${NC}\n"

# Init BUMP vars
bumped_cnt=0
TODAY=$(date +'%Y.%-m.%-d') # YYYY.M.D format

# Check LATEST COMMIT for extension changes
chromium_manifest_path=$(dirname "$MANIFEST_PATH" | sed 's|^\./||')
echo "Checking last commit details for $chromium_manifest_path..."
latest_platform_commit_msg=$(git log -1 --format=%s -- "$chromium_manifest_path")
if [[ $latest_platform_commit_msg =~ bump.*(ersion|manifest) ]] ; then
    echo -e "No changes found." ; exit ; fi 

echo "Bumping version in Chromium manifest..."

# Determine OLD/NEW versions
old_ver=$(sed -n 's/.*"version": *"\([0-9.]*\)".*/\1/p' "$MANIFEST_PATH")
if [[ $old_ver == "$TODAY" ]] ; then
     new_ver="$TODAY.1"
elif [[ $old_ver == "$TODAY."* ]] ; then
     LAST_NUMBER=$(echo "$old_ver" | awk -F '.' '{print $NF}')
     new_ver="$TODAY.$((LAST_NUMBER + 1))"
else new_ver="$TODAY" ; fi

# BUMP old version
sed -i "s/\"version\": \"$old_ver\"/\"version\": \"$new_ver\"/" "$MANIFEST_PATH"
echo -e "Updated: ${BW}v${old_ver}${NC} → ${BG}v${new_ver}${NC}\n"
((bumped_cnt++))

# COMMIT/PUSH bump
if (( $bumped_cnt == 0 )) ; then echo -e "${BW}Completed. No manifests bumped.${NC}"
else
    echo -e "${BY}Committing bump to Git...\n${NC}"
    git add ./**/manifest.json && git commit -n -m "Bumped \`version\` to $NEW_VER"
    git push
    echo -e "\n${BG}Success! Manifest updated/committed/pushed to GitHub${NC}"
fi
