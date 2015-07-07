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
    licence_record = {
        "source_url": raw_record['source_url'],
        "sample_date": raw_record["sample_date"],
        "category": ["Financial"],
        "licence_holder": {
            "entity_type": "company",
            "entity_properties": {
                "name": raw_record['name'],
                "mailing_address": raw_record['box'],
                "jurisdiction": raw_record['country'],
            }
        },
        "permissions": [],
        "licence_issuer": {
            "name": "Bank of Oman",
            "jurisdiction": "Oman",
        },
        "jurisdiction_of_licence": "Oman",
    }

    if raw_record['tel']:
        licence_record['licence_holder']['entity_properties']['telephone_number'] = raw_record['tel']

    if raw_record['fax']:
        licence_record['licence_holder']['entity_properties']['fax_number'] = raw_record['fax']

    print json.dumps(licence_record)
