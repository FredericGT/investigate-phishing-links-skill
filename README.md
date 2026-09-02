# Investigate Phishing Links — Codex Skill

A reusable Codex skill for safe, evidence-backed investigation of suspected phishing URLs.

用于安全分析疑似钓鱼链接的 Codex Skill，支持基础设施调查、受控静态/动态分析、IOC 提取、事件报告和证据打包。

## What it does / 功能

- Parse suspicious URLs, brand impersonation, paths, query parameters, and tracking tokens.
- Review DNS, RDAP/WHOIS, hosting, ASN, TLS certificates, and public infrastructure records.
- Record minimal HTTP status, headers, redirects, and response differences in an authorized isolated environment.
- Inspect saved HTML and JavaScript strictly as text for forms, external requests, fingerprinting, anti-automation, tracking, and download lures.
- Separate confirmed facts, high-confidence assessments, and unconfirmed attack stages.
- Generate technical reports, management briefs, weekly summaries, Jira incident records, IOC CSV/JSON, and evidence packages.
- Adapt containment and exposure-hunting guidance to the security tools the organization actually has.

## Safety boundaries / 安全边界

This skill is intended only for authorized defensive analysis. It instructs Codex to:

- Never submit usernames, passwords, MFA codes, cookies, OAuth consent, or payment data.
- Never execute or install downloaded binaries, scripts, documents, archives, or extensions.
- Never use an authenticated personal or corporate browser profile against the target.
- Never bypass CAPTCHA, anti-bot checks, conditional delivery, authentication, authorization, or rate limits.
- Never mutate victim tokens, enumerate paths, brute-force identifiers, exploit vulnerabilities, or probe unrelated infrastructure.
- Fall back to passive research and preserved evidence when a verified disposable environment is unavailable.

## Repository structure / 仓库结构

```text
investigate-phishing-links/
├── SKILL.md
├── VERSION
├── agents/openai.yaml
├── references/
│   ├── reporting-and-iocs.md
│   └── technical-workflow.md
├── scripts/
│   ├── build_evidence_package.py
│   └── ci_check.py
└── tests/test_build_evidence_package.py
```

The repository README is intentionally outside the Skill directory so the installed Skill contains only files required by Codex.

## Install / 安装

Ask Codex to install the skill from this repository path:

```text
Use $skill-installer to install:
https://github.com/FredericGT/investigate-phishing-links-skill/tree/main/investigate-phishing-links
```

For a manual installation, clone the repository and copy the `investigate-phishing-links` directory into `~/.codex/skills/`.

Private repositories require an authenticated GitHub session with access to the repository.

## Use / 使用

```text
Use $investigate-phishing-links to safely analyze this suspected phishing URL.
Do not submit credentials, execute downloads, or bypass access controls.
Generate a technical report, IOC files, and a Jira incident record.
```

中文示例：

```text
使用 $investigate-phishing-links 安全分析这个疑似钓鱼链接。
不要提交凭证、不要执行下载内容、不要绕过访问控制，并生成技术报告、IOC和Jira事件记录。
```

## Evidence packaging / 证据打包

`scripts/build_evidence_package.py` packages a reviewed case directory without executing its contents. It rejects symlinks, reads only regular files as bytes, adds a SHA-256 manifest, and creates a deterministic ZIP.

Review and redact the case directory before packaging. Keep raw URLs, tokens, personal information, internal telemetry, and untrusted HTML/JavaScript in access-restricted case storage.

## Local validation / 本地验证

Run the offline quality gates from the repository root:

```bash
python3 investigate-phishing-links/scripts/ci_check.py
```

The checks validate Skill metadata, compile the Skill's own Python files, and
run synthetic evidence-packaging tests. They do not contact a URL or execute
case content.

## Notes / 说明

- The Skill contains no real incident IOC, victim data, tracking token, credential, or malicious sample.
- A high-confidence phishing-gateway classification does not by itself prove credential theft, session hijacking, malware delivery, or endpoint compromise.
- Product-specific actions must be verified against deployed licenses, telemetry, and permissions before they are reported as feasible or complete.
