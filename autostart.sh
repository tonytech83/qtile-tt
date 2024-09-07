#!/usr/bin/env bash 

COLORSCHEME=Nord

### AUTOSTART PROGRAMS ###
picom --daemon &
nm-applet &
sleep 1
conky -c "$HOME"/.config/conky/qtile/Nord.conf || echo "Couldn't start conky."
feh --bg-fill "$HOME"/Pictures/wall/10.png
