# address_parser.py
import re

def parse_address(address):
    """
    Input: '123 N Main St, Madison, WI'
    Output: parsed parts
    """
    parts = address.split(',')
    street_part = parts[0].strip()
    municipality = parts[1].strip() if len(parts) > 1 else ""

    # Match format: house number + optional direction + street + type
    match = re.match(r'(\d+)\s+([NSEW])?\s*(\w+)\s+(\w+)', street_part)

    if match:
        house_number = match.group(1)
        prefix = match.group(2) or ""
        street_name = match.group(3)
        street_type = match.group(4)
    else:
        house_number = prefix = street_name = street_type = ""

    return {
        'house_number': house_number,
        'prefix': prefix,
        'street_name': street_name,
        'street_type': street_type,
        'municipality': municipality
    }
