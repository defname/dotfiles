#!/usr/bin/env bash

# uses maim for the screenshot and imagemagick for image manipulation

# do nothing if i3lock is already running
if [ -n "$(pidof i3lock)" ]; then echo "i3lock already running"; exit 0; fi

lighticon="$HOME/.config/i3/lock_light.png"
darkicon="$HOME/.config/i3/lock_dark.png"
tmpbg='/tmp/screen.jpg'

# take a screenshot
maim -u "$tmpbg"

# set a threshold value to determine if we should use the light icon or dark
# icon
VALUE="60" #brightness value to compare to

# determine the color of the screenshot
# thanks to [i3lock-fancy](https://github.com/meskarune/i3lock-fancy) for the
# idea of getting the background color to change the icons
COLOR=$(convert "$tmpbg" -gravity center -crop 100x100+0+0 +repage -colorspace hsb \
    -resize 1x1 txt:- | awk -F '[%$]' 'NR==2{gsub(",",""); printf "%.0f\n", $(NF-1)}');

# change the color ring colors to leave the middle of the feedback ring
# transparent and the outside to use either dark or light colors based on the 
# screenshot

if [ "$COLOR" -gt "$VALUE" ]; then #light background, use dark icon
    icon="$darkicon"
    PARAM=(--insidecolor=00000000 --insidevercolor=00000000 \
    --insidewrongcolor=00000000 --verifcolor=00000000 --wrongcolor=00000000 \
    --line-uses-inside --ringcolor=00000000 --ringvercolor=000000aa \
    --ringwrongcolor=e99393aa --bshlcolor=e99393aa --keyhlcolor=000000aa)
else # dark background so use the light icon
    icon="$lighticon"
    PARAM=(--insidecolor=00000000 --insidevercolor=00000000 \
    --insidewrongcolor=00000000 --verifcolor=00000000 --wrongcolor=00000000 \
    --line-uses-inside --ringcolor=00000000 --ringvercolor=ffffffaa \
    --ringwrongcolor=e99393aa --bshlcolor=e99393aa --keyhlcolor=ffffffaa)
fi

# blur the screenshot by resizing and scaling back up
convert "$tmpbg" -blur 0x8 "$tmpbg"
#convert "$tmpbg" -alpha set -channel A -evaluate set 50% png32:"$tmpbg"
# overlay the icon onto the screenshot
convert "$tmpbg" "$icon" -gravity center -composite "$tmpbg"

# lock the screen with the color parameters
i3lock "${PARAM[@]}" -i "$tmpbg"
exit 0


