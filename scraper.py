# -*- coding: utf-8 -*-

import json
import datetime
import re
import turbotlib

from bs4 import BeautifulSoup
import requests


turbotlib.log("Starting run...")


class Entry(object):
    def __init__(self):
        self.name = ''
        self.tel = ''
        self.fax = ''
        self.telex = ''
        self.swift = ''
        self.box = ''
        self.reuters = ''
        self.url = ''
        self.ceo_tel = ''
        self.ceo_fax = ''

patterns = (
    ('tel', '.*Tel(?:\.|:|\s+)? (.*)'),
    ('fax', '.*Fax(?:\.|:|\s+)? (.*)'),
    ('telex', '.*Telex(?:\.|:|\s+)? (.*)'),
    ('swift', '.*Swift(?:\.|:|\s+)? (.*)'),
    ('box', '.*Box(?:\.|:|\s+)? (.*)'),
    ('reuters', '.*Reuters(?:\.|:|\s+)? (.*)'),
    ('url', '(http://.*)'),
    ('ceo_tel', '.*CEO\'s Tel(?:\.|:|\s+)? (.*)'),
    ('ceo_fax', '.*CEO\'s Fax(?:\.|:|\s+)? (.*)'),
)


def parse_text(text, entry):
    for name, rx in patterns:
        m = re.match(rx, text, re.UNICODE)
        if m:
            setattr(entry, name, m.group(1).strip())


def fetch_data(url):
    response = requests.get(url)
    html = response.content

    doc = BeautifulSoup(html)
    table = doc.find(id="AutoNumber3")
    data_cell = table.find_all('td')[-1]

    entries = []
    current_entry = None

    for node in data_cell.children:
        if node.name == 'h1':
            if current_entry:
                entries.append(current_entry)
            current_entry = Entry()
            current_entry.name = re.sub(r'\s+', ' ', node.text)

        elif node.name == 'p':
            if len(node.find_all('br')) > 3:
                lines = node.text.split('\n')
                for line in lines:
                    parse_text(line.strip(), current_entry)
            else:
                text = node.text.strip()
                parse_text(text, current_entry)

    entries.append(current_entry)
    return entries

urls = [
    'http://www.cbo-oman.org/related_Allbanks.htm',
    'http://www.cbo-oman.org/related_specialBanks.htm',
    'http://www.cbo-oman.org/related_forign.htm',
    'http://www.cbo-oman.org/related_finance.htm',
    'http://www.cbo-oman.org/related_exchange.htm',
]

for url in urls:
    turbotlib.log("Scraping {}...".format(url))
    entries = fetch_data(url)

    for e in entries:
        print json.dumps(e.__dict__)
