#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: CLI client for Urban Dictionary
# Author: fkolacek@redhat.com
# Version: 0.1a
# Get token: https://market.mashape.com/community/urban-dictionary

import sys
import os
import requests
import re
from prettytable import PrettyTable
from prettytable import ALL as ALL

API_TOKEN = "--------------------------------------------------"
API_HOST = "https://mashape-community-urban-dictionary.p.mashape.com/define?term="

def formatString(data, maxLineLength):
    currentLength = 0
    words = data.split(" ")
    formattedString = ""
    for word in words:
        if currentLength + (len(word) + 1) <= maxLineLength:
            formattedString = formattedString + word + " "
            currentLength = currentLength + len(word) + 1
        else:
            formattedString = formattedString + "\n" + word + " "
            currentLength = len(word) + 1

    return formattedString

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "[!] Usage: %s [abbreviation]" % sys.argv[0]
        exit(1)

    headers = {
        'Accept': "text/plain",
        'X-Mashape-Key': API_TOKEN
    }

    query =  sys.argv[1]
    r = requests.get("%s%s" %(API_HOST, query), headers=headers)

    if r.status_code != 200:
        print "[!] Something went wrong, got %d from server!" % r.status_code
        exit(1)

    data = r.json()

    if len(data['list']) == 0:
        print "[*] Even Urban has no clue what does it mean!"
        exit(0)

    print "[*] Found %d definitions of %s:" % (len(data['list']), query)

    t = PrettyTable(['Name', 'Definition'])
    t.hrules=ALL
    t.align = 'l'

    for definition in data['list']:
        a = definition['author'].replace('\r\n', ' ')
        d = definition['definition'].replace('\r\n', ' ').replace('\t', ' ')

        t.add_row([a, formatString(d, 100)])

    print t
