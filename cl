#!/bin/bash

XCLIP=$(which xclip)

if [ -z "${XCLIP}" ]; then
  echo "Cannot find xclip in PATH"
  exit 1
fi

if [ -f "$1" ]; then
  cat "$1" | ${XCLIP} -selection clipboard
else
  echo "File does not exist!" | ${XCLIP} -selection clipboard
fi

