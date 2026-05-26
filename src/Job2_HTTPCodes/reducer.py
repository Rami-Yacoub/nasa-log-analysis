#!/usr/bin/env python3

import sys
from collections import defaultdict

code_counts = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        code, count = line.split('\t')
        code_counts[code] += int(count)
    except ValueError:
        continue

for code, count in sorted(code_counts.items()):
    print("{0}\t{1}".format(code, count))