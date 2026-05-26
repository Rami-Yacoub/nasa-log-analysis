#!/usr/bin/env python3

import sys
import re

pattern = re.compile(r'\[(\d{2}/\w{3}/\d{4}):(\d{2}):')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    match = pattern.search(line)
    if match:
        hour = match.group(2)
        print("{0}\t1".format(hour))