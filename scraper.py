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
        self.sample_date = str(datetime.date.today())
        self.source_url = ''
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
        self.country = ''

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
        m = re.match(rx, text, re.UNICODE | re.DOTALL)
        if m:
            text = m.group(1).strip()
            text = re.sub('\s+', ' ', text)
            setattr(entry, name, text)


def fetch_data(url, org_type, is_local):
    response = requests.get(url)
    html = response.content

    doc = BeautifulSoup(html)
    table = doc.find(id="AutoNumber3")
    data_cell = table.find_all('td')[-1]

    current_entry = None

    for node in data_cell.children:
        if node.name == 'h1':
            if current_entry:
                yield current_entry
            current_entry = Entry()
            current_entry.source_url = url
            current_entry.org_type = org_type
            current_entry.name = re.sub(r'\s+', ' ', node.text).strip()
            if is_local:
                current_entry.country = 'Oman'
            else:
                words = set(current_entry.name.split())
                common = words.intersection(country_names)
                if common:
                    current_entry.country = common.pop()

        elif node.name == 'p':
            if len(node.find_all('br')) > 3:
                lines = node.text.split('\n')
                for line in lines:
                    parse_text(line.strip(), current_entry)
            else:
                text = node.text.strip()
                parse_text(text, current_entry)

    yield current_entry


# List of pages to scrape - plus some extra metadata about them
pages = [
    {
        'url': 'http://www.cbo-oman.org/related_Allbanks.htm',
        'org_type': 'Local Banks',
        'is_local': True,
    },
    {
        'url': 'http://www.cbo-oman.org/related_specialBanks.htm',
        'org_type': 'Specialized Banks',
        'is_local': True,
    },
    {
        'url': 'http://www.cbo-oman.org/related_forign.htm',
        'org_type': 'Foreign Banks - Commercial Banks',
        'is_local': False,
    },
    {
        'url': 'http://www.cbo-oman.org/related_finance.htm',
        'org_type': 'Financial and Leasing Companies',
        'is_local': True,
    },
    {
        'url': 'http://www.cbo-oman.org/related_exchange.htm',
        'org_type': 'Money Exchange Companies',
        'is_local': True
    },
]

country_list = json.load(open('country.json'))
country_names = country_list.values()

for page in pages:
    turbotlib.log("Scraping {}...".format(page['url']))
    for e in fetch_data(**page):
        print json.dumps(e.__dict__)
