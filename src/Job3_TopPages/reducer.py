#!/usr/bin/env python3

import sys
from collections import defaultdict

url_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        url, count = line.split('\t', 1)
        url_counts[url] += int(count)
    except ValueError:
        continue

for url, count in sorted(url_counts.items(), key=lambda x: x[1], reverse=True):
    print("{0}\t{1}".format(url, count))