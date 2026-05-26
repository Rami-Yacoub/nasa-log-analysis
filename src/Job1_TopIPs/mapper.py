#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split(' ')
    if len(parts) > 0:
        ip = parts[0]
        print("{0}\t1".format(ip))