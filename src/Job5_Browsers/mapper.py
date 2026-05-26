#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Extraire le User-Agent
    parts = line.split('"')
    if len(parts) >= 6:
        user_agent = parts[5]
        
        # Identifier le navigateur
        browser = "Other"
        if "MSIE" in user_agent or "Trident" in user_agent:
            browser = "Internet Explorer"
        elif "Firefox" in user_agent:
            browser = "Firefox"
        elif "Chrome" in user_agent:
            browser = "Chrome"
        elif "Safari" in user_agent and "Chrome" not in user_agent:
            browser = "Safari"
        elif "Opera" in user_agent or "OPR" in user_agent:
            browser = "Opera"
        elif "Mozilla" in user_agent:
            browser = "Mozilla"
        
        print("{0}\t1".format(browser))