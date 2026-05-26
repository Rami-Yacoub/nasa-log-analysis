#!/usr/bin/env python3

import sys
import re

date_pattern = re.compile(r'\[(\d{2}/\w{3}/\d{4}):')
size_pattern = re.compile(r'" \d{3} (\d+)')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    date_match = date_pattern.search(line)
    size_match = size_pattern.search(line)
    
    if date_match and size_match:
        date = date_match.group(1)
        try:
            size = int(size_match.group(1))
            print("{0}\t{1}".format(date, size))
        except ValueError:
            continue