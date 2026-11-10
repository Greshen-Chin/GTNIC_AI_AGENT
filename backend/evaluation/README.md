# Request detector evaluation

`request_cases.v1.json` contains 34 explicitly labelled synthetic lab scenarios:
20 positive requests (SQLi, XSS, sensitive-file/traversal probes, command injection)
and 14 negative/control requests, including Juice Shop challenge telemetry.

Run from `backend`:

```powershell
python -m pytest tests/ -q
```

`GET /api/benchmark` executes the deployed detector against these cases and reports
the expected and actual category for every case, exact classification accuracy,
binary TP/TN/FP/FN, precision, recall, dataset hash and detector version. Statistics
expose this result for the dashboard's **Lab Detection Accuracy** card.

This is a small, developer-curated regression dataset. It is not a held-out
production study, a measurement of Gemini's narratives, or a claim that unseen
attacks will achieve the same score. No lab case is inserted as a live incident.
Real-world accuracy requires separately labelled attack and normal requests,
including missed detections; confidence scores do not supply those labels.

Evidence scores omit pending/failed investigations. HTTP status and matching
signatures do not establish exploitation success, database errors, or WAF action.
Analyst approvals record decisions without claiming external enforcement.

## Resetting the lab

Only an explicit workflow dispatch with `reset_lab: true`, or a deployment commit
whose message contains `[reset-lab]`, resets the lab. API and forwarder are stopped;
all incidents are copied to a timestamped `incidents_archive_*` table and counted
before clearing. The forwarder cursor advances to the current log end, then both
services restart. PostgreSQL and original access logs are retained.
