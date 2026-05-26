#!/usr/bin/env python3

import sys
from collections import defaultdict

hour_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        hour, count = line.split('\t')
        hour_counts[hour] += int(count)
    except ValueError:
        continue

for hour, count in sorted(hour_counts.items()):
    print("{0}h\t{1}".format(hour, count))