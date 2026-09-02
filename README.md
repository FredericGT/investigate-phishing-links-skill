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

---

## 中文详细说明

`investigate-phishing-links` 是一个面向授权防御调查的 Codex Skill，用于在
不提交凭证、不执行下载内容、不绕过访问控制的前提下分析疑似钓鱼链接、
登录页面、会议页面及已有证据包。

### 功能范围

- 离线解析 URL、域名、路径、查询参数、重定向参数和 tracking token。
- 调查 DNS、RDAP/WHOIS、注册时间、托管、ASN、TLS 证书和公开基础设施记录。
- 在明确授权且隔离环境可验证时，采集最小化的 HTTP 状态、响应头和重定向链。
- 将 HTML 和 JavaScript 作为文本分析，检查表单、外联、下载诱导、指纹和反自动化逻辑。
- 提取带角色和置信度的 IOC，并区分恶意基础设施、共享托管和正常跳转目标。
- 生成中文或英文技术报告、管理层简报、周报、Jira Markdown、IOC CSV/JSON 和证据 ZIP。

### 使用方式

```text
使用 $investigate-phishing-links 安全分析这个疑似钓鱼链接。
只做被动或经授权的受控分析，不提交凭证、不执行下载内容、不绕过访问控制，
并生成技术报告、IOC 和证据包。
```

### 安全边界

- 不提交用户名、密码、MFA、Cookie、OAuth 授权或支付信息。
- 不执行、安装、导入、预览或打开二进制、脚本、文档、归档或浏览器扩展。
- 不使用日常浏览器、企业 VPN、密码管理器或已认证会话接触目标。
- 不绕过 CAPTCHA、WAF、反自动化、地理限制、认证或访问控制。
- 不枚举路径、猜测 token、爆破、fuzz、利用漏洞或上传内容。
- 无法验证一次性隔离环境时，退回被动研究和已有证据静态分析。

### 结论等级

- `Confirmed`：由捕获的原始数据或权威记录直接支持。
- `High Confidence`：多个已确认指标共同支持的判断。
- `Not Confirmed`：没有直接证据的凭证提交、会话劫持、恶意软件执行或账号影响。

### 证据打包

```bash
python3 investigate-phishing-links/scripts/build_evidence_package.py \
  /absolute/path/to/reviewed-case \
  /absolute/path/to/case-package.zip
```

打包前必须先脱敏并审查案件目录。脚本拒绝 symlink 和非普通文件，拒绝覆盖已有
ZIP，并在 ZIP 内写入 SHA-256 manifest。

### 本地验证

```bash
python3 investigate-phishing-links/scripts/ci_check.py
```

测试使用合成案件文件，不访问真实 URL，也不执行案件内容。

### 可移植性

`SKILL.md` 的 `$investigate-phishing-links` 自动发现和调用是 Codex 机制；其他模型
可以显式加载该文件、参考文档和 Python 打包脚本，但不会自动识别这个命令。
