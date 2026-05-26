#!/usr/bin/env python3

import sys
from collections import defaultdict
from datetime import datetime

day_bandwidth = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        date, size = line.split('\t')
        day_bandwidth[date] += int(size)
    except ValueError:
        continue

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%b/%Y')
    except:
        return datetime.min

for date, total_bytes in sorted(day_bandwidth.items(), key=lambda x: parse_date(x[0])):
    print("{0}\t{1}".format(date, total_bytes))