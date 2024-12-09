#!/bin/bash

# Bumps extension manifest + git commit/push

# Init UI COLORS
NC="\033[0m"    # no color
BR="\033[1;91m" # bright red
BY="\033[1;33m" # bright yellow
BG="\033[1;92m" # bright green
BW="\033[1;97m" # bright white

# Init manifest PATH
manifest_path="chromium/extension/manifest.json"

# BUMP version
echo -e "${BY}\nBumping version in ${manifest}...${NC}\n"
bumped_cnt=0
TODAY=$(date +'%Y.%-m.%-d') # YYYY.M.D format
new_versions=() # for dynamic commit msg
old_ver=$(sed -n 's/.*"version": *"\([0-9.]*\)".*/\1/p' "$manifest")
if [[ $old_ver == "$TODAY" ]] ; then
     new_ver="$TODAY.1"
elif [[ $old_ver == "$TODAY."* ]] ; then
     LAST_NUMBER=$(echo "$old_ver" | awk -F '.' '{print $NF}')
     new_ver="$TODAY.$((LAST_NUMBER + 1))"
else new_ver="$TODAY" ; fi
new_versions+=("$new_ver")
sed -i "s/\"version\": \"$old_ver\"/\"version\": \"$new_ver\"/" "$manifest_path"
echo -e "Updated: ${BW}v${old_ver}${NC} → ${BG}v${NEW_VER}${NC}"
((bumped_cnt++))

# COMMIT/PUSH bump
if [[ $bumped_cnt -eq 0 ]] ; then echo -e "${BW}Completed. No manifests bumped.${NC}"
else
    echo -e "\n${BY}\nCommitting bump to Git...\n${NC}"
    git add ./**/manifest.json && git commit -n -m "Bumped \`version\` to $NEW_VER"
    git push

    # Print FINAL summary
    echo -e "\n${BG}Success! ${manifest} updated/committed/pushed to GitHub${NC}"
fi
