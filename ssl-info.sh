#!/bin/bash
# Author: fkolacek@redhat.com
# Description: 
# Version: 1.0

if [ "$1" == "" ]; then
  echo "[!] Usage: $0 [cert file]"
  exit 1
fi

if [ -f "$1" ]; then
  echo "[*] Retrieving information from $1"
  openssl x509 -text -in "$1"
else
  echo "[*] Connecting to $1:443"
  out=$(echo 'QUIT' | openssl s_client -showcerts -connect "$1:443" 2>&1)

  if [ -z "$2" ]; then
    echo "$out"
  else
    echo "$out" | openssl x509 -noout -text
  fi
fi

exit 0
