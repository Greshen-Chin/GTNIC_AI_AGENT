#!/usr/bin/env python3
import sys, json, requests

alert_file, token, hook_url = sys.argv[1], sys.argv[2], sys.argv[3]
with open(alert_file) as f:
    alert = json.load(f)
try:
    requests.post(hook_url, json=alert, timeout=10, headers={'X-Wazuh-Token': token})
except Exception as e:
    sys.stderr.write('custom-n8n error: %s\n' % e)
    sys.exit(1)
