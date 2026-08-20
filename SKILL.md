---
name: investigate-phishing-links
description: Safely investigate suspected phishing URLs and related evidence through passive infrastructure research, minimal isolated HTTP collection, static HTML/JavaScript analysis, IOC extraction, exposure-hunting guidance, and evidence-backed reporting. Use when Codex is asked to analyze a suspicious link or meeting/login page, explain its likely purpose, review an existing phishing evidence package, create technical or management reports, generate a Jira security incident, prepare SentinelOne-oriented follow-up, or package investigation evidence without executing untrusted content.
---

# Investigate Phishing Links

Investigate suspected phishing links without crossing into credential submission, payload execution, access-control bypass, or offensive testing. Produce conclusions that remain traceable to preserved evidence.

## Establish scope

1. Record the supplied URL exactly in restricted case evidence. Defang it in ordinary reports.
2. Record when and how the link was reported, the intended target, authorized scope, timezone, and permitted actions.
3. Determine the requested mode:
   - Review existing evidence only: do not contact the target.
   - Passive infrastructure research: inspect public DNS, RDAP/WHOIS, certificates, and public indexes.
   - Controlled live collection: require explicit authorization and a disposable isolated environment.
   - Reporting or packaging: operate only on preserved files.
4. Identify the organization's actual security stack before recommending controls. Do not assume Microsoft Defender, Entra, Google advanced investigation, SentinelOne licensing, or any other product capability.

## Enforce safety boundaries

- Never submit real or synthetic usernames, passwords, MFA codes, recovery data, cookies, OAuth consent, or payment data.
- Never execute, install, import, preview, or open downloaded binaries, scripts, documents, archives, browser extensions, or other active content.
- Treat captured HTML and JavaScript as untrusted bytes. Inspect them only as text with non-executing tools.
- Never use the user's normal browser profile, authenticated sessions, password manager, clipboard, corporate VPN identity, or existing cookies against the target.
- Do not bypass CAPTCHA, anti-bot checks, browser challenges, conditional delivery, geofencing, authentication, authorization, rate limits, or access controls.
- Do not mutate victim tokens, enumerate paths, brute-force identifiers, fuzz parameters, exploit vulnerabilities, upload content, or probe unrelated infrastructure.
- Limit authorized live collection to the smallest necessary GET/HEAD requests. Stop when the next step would submit a form, trigger a download, execute code, or defeat a screening mechanism.
- Do not visit a live target again when preserved evidence already answers the question.
- If an isolated disposable environment cannot be verified, fall back to passive research and static analysis.

## Run the investigation

Follow [technical-workflow.md](references/technical-workflow.md) for the detailed collection and analysis checklist.

Use this sequence:

1. Parse the URL offline: registrable domain, hostname, path, query keys, meeting/login pretext, brand similarity, redirect parameters, and recipient-like tokens.
2. Collect passive infrastructure evidence: DNS, RDAP/WHOIS, registration age, registrar, nameservers, hosting/ASN context, certificate subject/SAN/issuer/validity/fingerprint, and public scan/cache records.
3. When authorized and isolated, record minimal HTTP behavior: status, headers, redirect chain, content type, body length, cookies, caching, security headers, and response differences. Preserve each request condition; do not infer a single routing rule when multiple variables changed.
4. Analyze saved HTML/JavaScript as text: page title, visible pretext, forms and actions, input fields, external resources, network APIs, downloads, obfuscation, tracking, fingerprinting, headless/WebDriver checks, timers, reloads, and conditional branches.
5. Extract IOCs with roles and handling guidance. Distinguish malicious infrastructure from benign redirect destinations, shared-hosting IPs, local sinkhole addresses, and volatile challenge paths.
6. Build an attack-chain model that stops at the last observed stage. Do not invent the final credential page, malware family, or account compromise.
7. Map only evidence-supported MITRE ATT&CK techniques.
8. Design exposure hunting and response steps using tools the organization actually has. Mark license, telemetry, or policy dependencies instead of claiming unavailable capabilities.

## Calibrate conclusions

Separate every important claim into:

- **Confirmed:** directly supported by captured data or authoritative records.
- **High-confidence assessment:** strongly inferred from multiple confirmed indicators.
- **Unconfirmed:** plausible but not observed.

Use strong language for the infrastructure classification when evidence supports it, while keeping payload-specific claims bounded. A high-confidence phishing gateway classification does not prove that credentials were submitted, a session was stolen, or malware executed.

For user impact, distinguish:

- Link delivered but not opened.
- Link opened with no input, authorization, or download.
- Credentials or MFA entered.
- OAuth or other authorization granted.
- Content downloaded but not executed.
- Content executed or endpoint behavior observed.

## Preserve evidence

- Record UTC and local timestamps, request conditions, tool versions, failures, and environmental limitations.
- Preserve raw headers, bodies, certificates, DNS/RDAP responses, screenshots, public-index results, deobfuscation notes, and command output.
- Hash evidence files with SHA-256. Do not change originals after hashing; analyze copies.
- Store raw URLs, tokens, personal data, and untrusted content only in access-restricted case storage.
- Never expose a live malicious URL as a clickable link in a report.
- Use `scripts/build_evidence_package.py` only after reviewing the case directory for secrets and irrelevant files. The script reads regular files as bytes, rejects symlinks, creates a SHA-256 manifest, and writes a ZIP without executing content.

## Produce deliverables

Read [reporting-and-iocs.md](references/reporting-and-iocs.md) when creating reports, IOC files, Jira records, weekly summaries, or attachment packages.

Generate only what the user requests, commonly:

- Technical report with scope, evidence, findings, attack chain, risk, MITRE mapping, IOCs, limitations, and response guidance.
- Short management brief in the requested language and tone.
- Weekly security summary covering event time, immediate analysis, final judgment, and approved compensating controls.
- Jira security incident in Markdown with checkable follow-up and closure criteria.
- Machine-readable `iocs.csv` and `iocs.json`.
- Restricted evidence ZIP plus external SHA-256 file.

Keep management and Jira follow-up aligned with approved, feasible actions. Never state that a control was deployed, a log search was completed, or a user was remediated unless evidence confirms it.

Before delivery, proofread names, timestamps, timezone conversions, product names, IOC values, checkbox state, and obvious language errors. Revalidate JSON, CSV, hashes, and ZIP integrity after the final edit.

## Stop and escalate

Stop active work and report the boundary when:

- Authorization or target ownership is unclear.
- The next step requires credential entry, code execution, challenge bypass, token mutation, enumeration, or exploitation.
- The target begins an automatic binary/script/document download that cannot be safely preserved without opening it.
- Live testing would expose corporate identity, authenticated browser state, sensitive network location, or third-party data.
- Requested containment requires a product capability or permission that has not been verified.

Continue with passive evidence, preserved artifacts, reporting, and clearly scoped recommendations whenever those remain safe.
