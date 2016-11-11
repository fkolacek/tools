#!/bin/bash

args=""
dest=~/Screens
name=$(date +"screen-%Y-%m-%d-%H-%M-%S.png")

if [ ! -z "$1" ]; then
  args="$1"
fi


if [ ! -d "$dest" ]; then
  mkdir -p "$dest"
fi

gnome-screenshot -f "${dest}/${name}" $args

which up 2>&1 >/dev/null
if [ $? -eq 0 ]; then
  up "${dest}/${name}"
fi
