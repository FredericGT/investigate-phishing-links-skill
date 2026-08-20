# Technical workflow

Use only the sections required by the requested scope. Preserve raw output and record failures; an unavailable data source is a limitation, not evidence of safety.

## 1. Intake and URL decomposition

- Record the report/delivery time separately from the analysis time.
- Preserve the exact URL in restricted evidence and use a defanged form elsewhere.
- Identify the registrable domain, hostname, path, port, fragment, query keys, and apparent brand or workflow.
- Flag meeting IDs, email-like values, base64-like blobs, UUIDs, JWTs, campaign IDs, and recipient-like tokens without decoding or mutating them unless decoding is entirely offline and non-executing.
- Compare the hostname with the official brand domain by ownership and registrable domain, not visual similarity alone.

## 2. Passive infrastructure

Collect, when available:

- A, AAAA, CNAME, NS, MX, TXT, CAA, SOA, DNSSEC status, TTLs, and independent resolver results.
- RDAP/WHOIS creation, update, expiry, registrar, status, nameservers, privacy service, and DNSSEC.
- IP allocation, ASN, reverse DNS, hosting provider, and shared-hosting indicators.
- TLS leaf subject, SANs, issuer, serial, validity, SHA-256 fingerprint, and chain behavior.
- Certificate Transparency, public scan, reputation, and web-cache records.

Treat these carefully:

- A young domain, privacy proxy, missing DNSSEC, or valid TLS certificate is contextual evidence, not standalone proof of phishing.
- A shared-hosting IP is usually suitable for hunting, not unconditional blocking.
- A local interception/sinkhole/test-range address is not an attacker IOC.
- Public-scan results may represent different times, locations, tokens, or client conditions.

## 3. Minimal isolated HTTP collection

Proceed only with explicit authorization and a verified disposable environment.

- Start with the exact supplied URL. Do not invent neighboring paths or identifiers.
- Record request time, resolved IP, SNI/Host, user agent, method, redirect policy, TLS verification mode, and proxy/isolation context.
- Save response status, headers, body bytes, body hash, content type, size, cookies, refresh behavior, and redirect location.
- Preserve every redirect hop. Mark official benign destinations as such.
- Compare a small number of ordinary client profiles only when needed to establish response variance. Do not spoof a victim, bypass a challenge, or iterate until a payload appears.
- If TLS verification fails, preserve the failure. Do not silently disable verification. If an explicitly authorized capture uses relaxed verification, record the fixed IP, SNI/Host, certificate, reason, and follow-up strict verification.
- Stop before submitting forms, calling constructed challenge endpoints, following download prompts, or progressing beyond conditional screening.

Do not claim a specific routing rule when user agent, cookies, time, token state, IP, or other variables changed together. State only that conditional or state-dependent behavior was observed.

## 4. Static HTML and JavaScript analysis

Inspect saved content as text. Do not open it in a browser or import it as a module.

Record:

- Page title, visible text, logos, brand assets, form fields, form methods/actions, buttons, iframes, links, and download attributes.
- Inline/external scripts, styles, images, fonts, third-party resources, fetch/XHR/WebSocket/beacon destinations, and same-origin challenge endpoints.
- Redirects, refresh timers, delayed execution, hidden forms, local/session storage, cookies, service workers, clipboard use, and notification requests.
- Fingerprinting and anti-analysis checks: WebDriver, headless user agents, plugins, MIME types, languages, screen/window dimensions, canvas/WebGL/audio, timezone, hardware concurrency, permissions, prototype integrity, devtools checks, and automation-specific globals.
- Obfuscation: string tables, encoded literals, dynamic property access, eval-like construction, packed scripts, and control-flow flattening. Deobfuscate only with text transformations; never evaluate the result.
- Tracking: original-URL forwarding, token propagation, unique IDs, analytics parameters, timestamps, and failed-check reporting.

Explicitly state whether credentials fields, MFA/OTP fields, OAuth consent, external data collection, or downloadable payloads were actually observed.

## 5. Attack-chain assessment

Model only observed and bounded inferred stages:

```text
delivery channel
  -> supplied URL and recipient/campaign token
  -> redirect, screening, or verification stage
  -> fingerprinting / anti-automation / state routing
  -> last observed endpoint
  -> possible later objectives (label as unconfirmed)
```

Use evidence to distinguish phishing gateway, benign redirect, credential capture, OAuth consent phishing, fake update/download, malware delivery, and tracking-only behavior.

## 6. Exposure hunting and response

First inventory available telemetry and permissions. Typical sources include EDR, DNS, proxy/SWG, firewall, managed browser, email, chat, SIEM, identity, and SaaS audit logs.

- Search the exact URL, domain, hostname, path, token, resolved IP, SNI, certificate fingerprint, and short-lived challenge paths.
- Correlate a suspicious-domain visit with immediate official-brand redirects, browser downloads, new files, and browser child processes.
- Avoid claiming that email delivery proves a click, or that a DNS lookup proves successful page rendering.
- For click-only cases, inspect the endpoint and download history without declaring infection.
- For entered credentials/MFA, require credential reset and use available identity controls to invalidate sessions or tokens only when the organization has those capabilities.
- For executed content or suspicious endpoint behavior, isolate through the available EDR and preserve the process/network timeline.

Translate recommendations into the organization's confirmed tools. If SentinelOne is available, describe domain/URL blocking, Deep Visibility hunting, Storyline review, download/process checks, or device isolation only to the extent supported by the deployed license and permissions.

## 7. Quality checks

- Verify every high-impact statement against raw evidence.
- Check timestamps and timezone conversions.
- Defang malicious URLs in human-facing text.
- Mark benign official redirect domains as do-not-block.
- Flag shared IPs and volatile paths as hunt-only where appropriate.
- Make limitations visible without weakening supported infrastructure-level conclusions.
- Ensure follow-up actions match the user's approved control set and are not reported as completed prematurely.
