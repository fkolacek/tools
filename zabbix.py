#!/usr/bin/env python
# pip install py-zabbix

from pyzabbix import ZabbixAPI
from prettytable import PrettyTable
from prettytable import ALL as ALL
from datetime import datetime
from datetime import timedelta

ZBX_HOST = "https://example.com/zabbix"
ZBX_USER = "guest"
ZBX_PASS = ""

class bcolors:
    INFORMATION = '\033[36m'
    WARNING = '\033[33m'
    AVERAGE = '\033[1m\033[33m'
    HIGH = '\033[31m'
    DISASTER = '\033[1m\033[31m'
    ENDC = '\033[0m'

def getDescription(priority, description):
  priority = int(priority)

  if priority == 1:
      STARTC = bcolors.INFORMATION
  elif priority == 2:
      STARTC = bcolors.WARNING
  elif priority == 3:
      STARTC = bcolors.AVERAGE
  elif priority == 4:
      STARTC = bcolors.HIGH
  elif priority == 5:
      STARTC = bcolors.DISASTER
  else:
      STARTC = ''

  return STARTC + description + bcolors.ENDC

def getLastChange(lastchange):
  return datetime.fromtimestamp(int(lastchange)).strftime('%Y-%m-%d %H:%M:%S')

def getAge(lastchange):
    td = datetime.now() - datetime.fromtimestamp(int(lastchange))

    output = ""
    if td.days:
      output += "%dd " % td.days
    if (td.seconds//3600) > 0:
      output += "%dh " % (td.seconds//3600)
    if ((td.seconds//60)%60) > 0:
      output += "%dm" % ((td.seconds//60)%60)

    return output

def getStats(stats):
    total = 0
    for stat in stats:
      total += int(stat)

    output = "Total problems: %d" % total
    return output

if __name__ == "__main__":
  zapi = ZabbixAPI(url=ZBX_HOST, user=ZBX_USER, password=ZBX_PASS)

  recentProblems = zapi.trigger.get(
    selectHosts = 'extend',
    selectItems = 'extend',
    monitored = 'true',
    only_true = 'true',
    value = 1,
    sortfield = ['lastchange'],
    sortorder = 'DESC'
  )

  t = PrettyTable(['Host', 'Issue', 'Last change', 'Age'])
  t.hrules=ALL
  t.align = 'l'

  stats = { '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 }

  for problem in recentProblems:
    for host in problem['hosts']:
        t.add_row([ host['host'], getDescription(problem['priority'], problem['description']), getLastChange(problem['lastchange']), getAge(problem['lastchange']) ])
        stats[problem['priority']] += 1

  print t
  print getStats(stats)

