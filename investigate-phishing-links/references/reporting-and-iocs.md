# Reporting and IOC formats

## Technical report

Use this order when a full report is requested:

1. Case metadata: report time, analysis window, target, analyst, exact defanged URL, authorization, and risk rating.
2. Executive conclusion.
3. Scope and safety boundaries.
4. Confirmed findings, high-confidence assessment, and unconfirmed items.
5. Timeline.
6. DNS, registration, hosting, and TLS.
7. HTTP and redirect behavior.
8. HTML/JavaScript static analysis.
9. Tracking-token and conditional-delivery analysis.
10. Brand impersonation evidence.
11. Observed/bounded attack chain.
12. Risk rationale.
13. Evidence-supported MITRE ATT&CK mapping.
14. IOC table and handling priority.
15. Exposure-hunting and response guidance for available tools.
16. Limitations.
17. Evidence index and hashes.

Do not present a scanner score as stronger evidence than manually verified behavior. Do not turn a likely objective into an observed victim impact.

## Management brief

Keep it conversational and short:

- What the site is.
- When it appeared or was reported.
- What controlled analysis confirmed.
- What the site does in plain language.
- What the organization will do next.

Mention uncertain payload details only when necessary for a decision. Keep infrastructure classification strong when supported, and avoid claiming confirmed credential theft, session hijacking, or malware execution without direct evidence.

## Weekly summary

Use one short incident paragraph plus approved measures:

```markdown
On <reported time>, the company received <delivery type> targeting <role/group>.
The security team immediately treated it as <classification> and performed <safe analysis categories> in an isolated environment.
The investigation concluded <evidence-backed plain-language judgment>.

Next actions:
1. <confirmed feasible containment>
2. <confirmed feasible exposure review and conditional remediation>
3. <awareness or process improvement>
```

Keep the report time separate from the later analysis window.

## Jira security incident

Include:

- Title, type, priority, status, report time, analysis window, target group, owner, and labels.
- Event summary and defanged indicator.
- Confirmed findings and risk rationale.
- Completed analysis checklist using checked boxes.
- Approved follow-up using unchecked boxes.
- Primary IOC table and do-not-block warnings.
- Evidence-supported MITRE mapping.
- Attachment inventory and evidence-handling warning.
- Closure criteria tied to the approved actions.

Do not include personal names unless necessary and authorized. Do not claim an action is complete unless it was verified.

## IOC CSV schema

Use UTF-8 with this header:

```csv
indicator,type,confidence,role,recommended_action,notes
```

Allowed confidence values should be consistent, for example: `high`, `medium`, `low`, `benign`, `not-an-ioc`.

Recommended actions should distinguish `block-and-hunt`, `hunt`, `hunt-before-blocking`, `do-not-block`, and `evidence-only`.

Example values must use reserved or defanged placeholders:

```csv
phish.example,domain,high,phishing-gateway,block-and-hunt,Example only
203.0.113.10,ipv4,medium,shared-hosting-origin,hunt-before-blocking,Documentation range
hxxps://login[.]example/path?token=REDACTED,url,high,campaign-link,block-and-hunt,Defanged example
```

## IOC JSON schema

```json
{
  "case_id": "CASE-YYYY-NNN",
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "indicators": [
    {
      "indicator": "phish.example",
      "type": "domain",
      "confidence": "high",
      "role": "phishing-gateway",
      "recommended_action": "block-and-hunt",
      "notes": "Example only"
    }
  ]
}
```

Validate JSON and CSV syntax before delivery.

## Evidence package

Recommended contents:

```text
case-package/
  case-summary.md
  technical-report.md
  jira-incident.md
  iocs.csv
  iocs.json
  evidence/
    README.md
    dns/
    rdap/
    tls/
    http/
    static/
  PACKAGE_SHA256SUMS.txt
```

Keep raw evidence restricted. Add a prominent warning when HTML, JavaScript, binaries, documents, full URLs, tokens, credentials, personal data, or internal telemetry are present. Verify the final ZIP independently and provide its SHA-256 in a separate file.
