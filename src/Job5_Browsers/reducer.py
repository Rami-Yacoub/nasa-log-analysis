#!/usr/bin/env python3

import sys
from collections import defaultdict

browser_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        browser, count = line.split('\t')
        browser_counts[browser] += int(count)
    except ValueError:
        continue

for browser, count in sorted(browser_counts.items(), key=lambda x: x[1], reverse=True):
    print("{0}\t{1}".format(browser, count))