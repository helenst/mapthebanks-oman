# -*- coding: utf-8 -*-

import json
import datetime
import re
import turbotlib

from bs4 import BeautifulSoup
import requests


turbotlib.log("Starting run...")

local_banks_url = 'http://www.cbo-oman.org/related_Allbanks.htm'

#response = requests.get(local_banks_url)
#html = response.content

html = open('oman.html')
doc = BeautifulSoup(html)
table = doc.find(id="AutoNumber3")
data_cell = table.find_all('td')[1]


class Entry(object):
    def __init__(self):
        self.name = ''
        self.tel = ''
        self.lines = []


entries = []
current_entry = None

for node in data_cell.children:
    if node.name == 'h1':
        if current_entry:
            entries.append(current_entry)
        current_entry = Entry()
        current_entry.name = re.sub(r'\s+', ' ', node.text)

    elif node.name == 'p':
        text = node.text.strip()
        m = re.match('.*Tel(\.|:|\s+)? (.*)', text, re.UNICODE)
        if m:
            #import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
            g = current_entry.tel = m.group(2)

        current_entry.lines.append(node.text)

entries.append(current_entry)

print [(e.name, e.tel) for e in entries]
#print entries[0].lines
tel = 'Tel&nbsp;&nbsp; 24768888'
