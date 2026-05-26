#!/usr/bin/env python3

import sys
from collections import defaultdict

ip_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        ip, count = line.split('\t')
        ip_counts[ip] += int(count)
    except ValueError:
        continue

for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
    print("{0}\t{1}".format(ip, count))