# cost_observer

Purpose: Track API spend, token use, source counts, and run health.

Required artifacts:
- manifest.json
- usage.tsv
- raw request/response JSON
- cards JSON

Alert conditions:
- parse failure
- missing source_url
- low confidence spike
- unexpected token/cost jump
