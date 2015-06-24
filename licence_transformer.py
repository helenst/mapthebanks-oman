"""
Transformer from primary data to licence schema

Data from http://www.cbo-oman.org/related.htm
Mission: https://missions.opencorporates.com/missions/761
"""
import sys
import json

while True:
    line = sys.stdin.readline()
    if not line:
        break
    raw_record = json.loads(line)

    # Can't have an empty country jurisdiction due to schema restrictions
    # so have to leave out the whole row.
    if raw_record['country']:
        licence_record = {
            "source_url": raw_record['source_url'],
            "company_name": raw_record['name'],
            "company_jurisdiction": raw_record['country'],
            "sample_date": raw_record["sample_date"],
            "licence_jurisdiction": "Oman",
            "category": "Financial",
        }

        print json.dumps(licence_record)
