#!/usr/bin/env python3

import sys
import re

pattern = re.compile(r'"[A-Z]+ (.+?) HTTP')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    match = pattern.search(line)
    if match:
        url = match.group(1)
        print("{0}\t1".format(url))