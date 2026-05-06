---
applyTo: "**/*.k6.js,**/k6/**/*.js,**/*k6*.js,output/**/*.js"
---

# k6 Script Generation Instructions

## Input Confirmation
- Before generating or changing any k6 script, ask for all required parameters:
  - Base URL / environment target
  - Endpoint(s), method(s), and required headers
  - Authentication mechanism and token source
  - Load profile (vus/rps, ramp-up, duration)
  - Performance thresholds (p95, error rate, throughput)

## Script Rules
- Use environment variables for URL, tokens, and credentials.
- Do not hardcode secrets in source files.
- Include checks for status code and critical response fields.
- Include thresholds for latency and error rate.
- Keep scenarios explicit and named.

## Reporting Requirements
- Every k6 execution must generate report artifacts automatically.
- Always export JSON summary with `--summary-export`.
- Always export HTML report with `K6_WEB_DASHBOARD=true` and `K6_WEB_DASHBOARD_EXPORT`.
- Use timestamped filenames per run to avoid overwriting previous results.
- Include a request summary artifact per run (JSON or CSV) with, at minimum:
  - method
  - URL or endpoint
  - status code
  - response time
  - error message when request fails
  - response body
- Always include in the report output a dedicated section with concrete response examples from the run.
- That section must include at least 100 full response examples when the run has 100 or more requests.
- If the run has fewer than 100 requests, include all available full responses.
- Each stored example must include at minimum: method, endpoint/URL, status code, response time, response headers, and full response body.

## Execution Safety
- Start with a smoke run before high load.
- Avoid destructive load against production without explicit approval.
- If required inputs are missing, stop and request them.
