#!/bin/env bash

INTERNAL_SCREEN="eDP1"
EXTERNAL_SCREEN="DP1"
TMPFILE="/tmp/monitor_mode"


if [ ! -f "$TMPFILE" ]; then
	xrandr --verbose --output "$EXTERNAL_SCREEN" --auto --right-of $INTERNAL_SCREEN --scale 2x2
	touch "$TMPFILE"
else
	xrandr --verbose --output "$EXTERNAL_SCREEN" --off
	rm "$TMPFILE"
fi
