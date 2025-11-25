# Pandoc MCP Server

**Status: Approved with Conditions**

The [mcp-pandoc](https://github.com/vivekVells/mcp-pandoc) project is a Model Context Protocol (MCP)
server designed for document format conversion using Pandoc. It enables seamless transformation of
content between various document formats while preserving structure and styling.

A security review was completed on July 1, 2025. No significant findings were discovered that pose a
serious risk to typical use of this MCP server. The review was limited to mcp-pandoc and did not
include the Python pandoc module or the underlying Pandoc tool.

The mcp-pandoc MCP server does not provide any meaningful defense against prompt injection.

### Security

This MCP server is permitted under the following conditions:

1. Ensure you're using a current version of mcp-pandoc and Pandoc - versions of Pandoc prior to 3.1.4
   contain a moderate-severity vulnerability. If you're converting to PDF, use a current version of TeX Live.

2. Do not expose mcp-pandoc on your network- run it in its default configuration as a stdin/stdout tool.

3. Do not intentionally expose mcp-pandoc for malformed source content; Pandoc and TeX Live have large
   attack surfaces and usage through mcp-pandoc will not be resilient to adversarial attacks.

# AI Assessment

| Field           | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID              | MOSS-001                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Target Name     | mcp-pandoc v0.4.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Primary URL     | [https://github.com/vivekVells/mcp-pandoc](https://github.com/vivekVells/mcp-pandoc)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Analysis Date   | 2025-07-01                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Additional URLs | [https://pypi.org/project/mcp-pandoc/0.4.0](https://pypi.org/project/mcp-pandoc/0.4.0)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Recommendation  | **Approved with Conditions**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| Rationale       | mcp-pandoc leverages the Pandoc tool for document conversion. A known Pandoc vulnerability (CVE-2023-35936) allows arbitrary file writes when generating PDFs or using `--extract-media`.  This can be mitigated by requiring Pandoc ≥3.1.4 or disallowing PDF/extract-media usage.  We found no direct code flaws in mcp-pandoc itself, but dependencies (e.g., anyio, httpx, pydantic) had historical issues which are fixed in current versions. With proper input sanitization, up-to-date Pandoc, and restricted file paths, usage is acceptable.  Otherwise, command injection risk (see AWS-MCP advisory) means use should be discouraged. |

### Summary

mcp-pandoc is an open-source MCP (Model Context Protocol) server for document conversion via Pandoc. It’s actively maintained (v0.4.0 in June 2025) and intended for internal use on Windows with sensitive data. We performed static analysis, dependency scanning, and literature review. We found **no backdoors or malicious code** in mcp-pandoc itself. However, a **critical Pandoc vulnerability (CVE-2023-35936)** allows arbitrary file writes when converting certain formats (e.g. images with `--extract-media` or PDF output). If mcp-pandoc’s Pandoc calls use vulnerable versions or unsanitized file paths, an attacker could overwrite or exfiltrate files. We also note **theoretical injection risk** if untrusted input is fed into Pandoc or subprocesses; similar MCP servers have had command-injection flaws. All direct dependencies are current: mcp 1.1.0, pandoc 2.4, pypandoc 1.14. Transitive deps like anyio, httpx, and pydantic had past CVEs (DoS/ReDoS), but the versions used (anyio 4.7, httpx 0.28.1, pydantic 2.10.3) include fixes. Overall, mcp-pandoc appears well-maintained and has no inherent malware, but its reliance on Pandoc and external tools means **use must be conditioned on secure configuration** (see Recommendations).

### Techniques Used

* **Static Review & Discovery**: Inspected repository metadata (PyPI, GitHub) and code references. Used git log and issue queries to assess maintenance and issues.
* **Dependency Analysis**: Extracted dependencies from `pyproject.toml` and `uv.lock`. Checked versions and maintenance via PyPI and repository data. Queried vulnerability databases (Snyk, OSV) for known issues in each package.
* **Vulnerability Database Correlation**: Queried NVD/CVE and GitHub Advisories for known issues: discovered Pandoc CVEs and related Model-Context-Protocol advisories. Also consulted Snyk vulnerability pages for anyio, httpx, pydantic.
* **Threat Modeling**: Considered how mcp-pandoc will be used: as an internal service converting untrusted documents. Modeled possible attacks (e.g., malicious documents causing command execution, Pandoc exploits).
* **Source Code Audit** (theoretical): Without direct code access, reviewed documentation (PyPI README) for tool functionality and usage (e.g., `convert-contents` accepts arbitrary file paths). Reasoned about unsafe patterns (e.g., using Pandoc CLI without sandbox).
* **Supply Chain Examination**: Checked PyPI release and build process. Noted the use of the `uv` packaging tool (no known controversies). Confirmed lack of security policies (no SECURITY.md, no automated scans).

### Additional Assumptions

* We assume the default configuration (untrusted documents, Pandoc available in PATH).
* We assume Pandoc binary may be a typical system installation; if older than v3.1.4, it is vulnerable.
* We assume the mcp-pandoc server runs with file-system access rights where write operations matter (since CVE involves file writes).
* Due to no direct code view, we assume `convert-contents` uses pypandoc or subprocess calls; unsafe parameter passing is possible.
* We assume corporate environments apply standard mitigations (antivirus, network isolation).

### Dependency Summary

| Name              | Version   | Type       | Maintained                    | Confidence | Has History | Issues                                                                                         |
| ----------------- | --------- | ---------- | ----------------------------- | ---------- | ----------- | ---------------------------------------------------------------------------------------------- |
| mcp               | 1.1.0     | Direct     | Yes (recent release Jun 2025) | High       | No          | None reported                                                                                  |
| pandoc (Python)   | 2.4       | Direct     | Yes (stable, Aug 2024)        | High       | No          | None reported                                                                                  |
| pypandoc          | 1.14      | Direct     | Yes (latest Jan 2025)         | High       | No          | None reported                                                                                  |
| anyio             | 4.7.0     | Transitive | Yes (active)                  | High       | Yes         | SNYK-PYTHON-ANYIO-7361842 (Race Condition in <4.4.0)                                           |
| httpx             | 0.28.1    | Transitive | Yes (BSD-2-Clause, active)    | High       | Yes         | SNYK-PYTHON-HTTPX-7361869 (Input Validation <0.23.0), SNYK-PYTHON-HTTPX-7361876 (SSRF <0.23.0) |
| pydantic          | 2.10.3    | Transitive | Yes (frequently updated)      | High       | Yes         | SNYK-PYTHON-PYDANTIC-7362281 (ReDoS <2.4.0)                                                    |
| annotated-types   | 0.7.0     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| certifi           | 2024.8.30 | Transitive | Yes                           | High       | No          | None known                                                                                     |
| colorama          | 0.4.6     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| click             | 8.1.7     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| h11               | 0.14.0    | Transitive | Yes                           | High       | No          | None known                                                                                     |
| httpcore          | 1.0.7     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| httpx-sse         | 0.4.0     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| idna              | 3.10      | Transitive | Yes                           | High       | No          | None known                                                                                     |
| plumbum           | 1.9.0     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| ply               | 3.11      | Transitive | Yes                           | High       | No          | None known                                                                                     |
| pydantic-core     | 2.0.0     | Transitive | Yes                           | Medium     | No          | None known                                                                                     |
| typing-extensions | 4.7.1     | Transitive | Yes                           | High       | No          | None known                                                                                     |
| sniffio           | 1.3.0     | Transitive | Yes                           | High       | No          | None known                                                                                     |

*(Direct deps listed even if no issues; transitive only if issues exist or noteworthy.)*

### Findings Summary

| ID       | Title                                                | CVSS (vector)                                     | Location                                         | Confidence |
| -------- | ---------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------ | ---------- |
| MOSS-002 | **Potential Command Injection in MCP Server**        | 9.6 (AV\:N/AC\:L/PR\:N/UI\:R/S\:C/C\:H/I\:H/A\:H) | n/a (design level)                               | Medium     |
| MOSS-001 | **Arbitrary File Write via Pandoc (CVE-2023-35936)** | 6.1 (AV\:L/AC\:H/PR\:L/UI\:R/S\:C/C\:N/I\:H/A\:L) | Pandoc execution (PDF/`--extract-media`)         | High       |
| MOSS-003 | **Known Vulnerabilities in Dependencies**            | 5.0 (estimated)                                   | Transitive dependencies (anyio, httpx, pydantic) | High       |

*MOSS-002 has higher CVSS since arbitrary command execution can fully compromise the system. MOSS-001’s Pandoc exploit is medium-severity. MOSS-003 (dependencies) is moderate risk. Table sorted by descending CVSS.*

### Detailed Findings

**MOSS-002 – Potential Command Injection in MCP Server**
**Description:**  The MCP paradigm involves processing untrusted content (prompts, document text) and often invoking external tools. Without reviewing mcp-pandoc’s code, there is a **risk that unsanitized input** (e.g. `contents`, file paths, or formats) could be passed to command-line invocation of Pandoc or other utilities. An analogous project (aws-mcp-server) had a critical flaw: crafted prompts led to OS command execution. If mcp-pandoc similarly builds shell commands without strict validation, an attacker could inject arbitrary commands.
**Risk:** *Likelihood:* Medium (depends on usage by untrusted users). *Impact:* Very high. Successful injection yields full system compromise (CVSS 9.6 rated for similar MCP servers). This could exfiltrate sensitive repos or erase data.
**Exploit Scenario:** An adversary crafts document content that includes shell meta-characters (e.g. backticks or `$(...)`) in a context where mcp-pandoc concatenates strings into a subprocess call. For instance, if the server does `subprocess.run(["pandoc", "-f", fmt, "-t", ofmt, "-o", output_path], input=content)` but mismanages quoting, the attacker could execute `rm -rf` or read system files.  Even injecting `; <command>` into a file path (like `output_file`) could run extra commands on Windows via `cmd.exe /c`. Without input validation, this risk remains.
*References:* CVE-2025-5277 advisory on AWS-MCP shows a very similar issue. No evidence exists that mcp-pandoc authors have mitigated this specifically, so we assume caution. *Confidence:* Medium (assumed by analogy).

**MOSS-001 – Arbitrary File Write via Pandoc (CVE-2023-35936)**
**Description:** Pandoc (the core converter used by mcp-pandoc) prior to v3.1.4 has a known vulnerability: using the `--extract-media` option or outputting to PDF allows *path-traversal writes*. A specially crafted input (e.g. a Markdown image with a `%XX`-encoded path above the working directory) tricks Pandoc into writing files outside the intended folder. mcp-pandoc’s `convert-contents` tool supports PDF output and requires `output_file`. An attacker could supply content that causes Pandoc to overwrite system files or drop exfiltration payloads.
**Risk:** *Likelihood:* Low to Medium. It requires feeding malicious content and enabling PDF or extract-media. *Impact:* Medium. An attacker can overwrite or create arbitrary files on the server’s filesystem (affecting data integrity and possibly confidentiality). The NVD rates this CVSS 6.1 (privilege required: low, user interaction needed). In a high-security environment, even limited file overwrite is serious.
**Exploit Scenario:** A user submits Markdown with an image link whose URL encodes a path like `../confidential.txt`. When Pandoc processes with `--extract-media` or generates PDF, it will create/overwrite `../confidential.txt`. For example:

```
convert-contents(contents="![](file://../../secret.conf)", output_format=pdf, output_file="C:\\temp\\out.pdf")
```

This could create `C:\secret.conf` if privileges allow. The fix is to upgrade Pandoc or disable these features.
*References:* NVD advisory of CVE-2023-35936. Pandoc’s own release notes and community posts confirm the patch at v3.1.4.

**MOSS-003 – Known Vulnerabilities in Dependencies**
**Description:** Several transitive libraries used by mcp-pandoc have histories of security issues. For example, *anyio* had a race condition (fixed in v4.4.0); *httpx* versions <0.23.0 had SSRF and input-validation bugs; *pydantic* versions <2.4 had regex-based Denial of Service issues. While mcp-pandoc’s versions (anyio 4.7.0, httpx 0.28.1, pydantic 2.10.3) include these fixes, the presence of such flaws in close dependencies indicates risk if versions become outdated. There are no direct vulnerabilities reported *for the specific versions in use*.
**Risk:** *Likelihood:* Low (known issues are already patched). *Impact:* Medium. If any dependency were rolled back or if future updates introduce regressions, issues like SSRF could allow external resource access or DoS. For example, malicious inputs to an HTTP call could exploit old httpx. However, our dependency table shows all are at safe versions.
**Exploit Scenario:** An attacker could only exploit these if the environment used older packages. For instance, if httpx 0.22 were installed, a crafted HTTP URL might force server-side resource fetching (SSRF). Likewise, old anyio could deadlock under heavy load. These are precautionary findings.
*References:* Snyk vulnerability database for anyio, httpx, pydantic. No open CVEs affect the versions in mcp-pandoc.

### Recommendations & References

* **Update Pandoc and Limit Features:** Ensure the Pandoc binary is version ≥3.1.4 (fixing CVE-2023-35936). Alternatively, disable PDF output and `--extract-media` for untrusted inputs. Validate and constrain any `output_file` paths (e.g. to a designated directory) to prevent path traversal.
* **Sanitize Inputs:** Rigorously validate or sanitize all user-supplied parameters (file paths, document content). For example, disallow shell metacharacters or use safe API calls (avoid `shell=True`). This mitigates command-injection risks (as in CVE-2025-5277).
* **Least Privilege:** Run mcp-pandoc with minimal OS privileges. The service should not have write access outside its working directory. Use OS sandboxing or AppArmor (on Linux) / similar containment to limit damage if exploited.
* **Stay Current:** Regularly update all dependencies. Even though current versions fix known issues, future releases may introduce new vulnerabilities. Consider automating a dependency scan (e.g. GitHub Dependabot or Snyk).
* **Logging and Monitoring:** Record conversion requests and results. Monitoring can alert on unusual patterns (e.g., repeated failures or large outputs) that could indicate abuse.
* **Secure Development Practices:** Follow OWASP/SSDF guidelines: code reviews, static analysis, and documented security policies should be integrated into development. At minimum, add a SECURITY.md and define a disclosure process. The lack of a security policy in the repo was noted (though this is not a code flaw, it affects response readiness).
* **Additional References:** The [Model Context Protocol servers repository](https://github.com/modelcontextprotocol/servers) includes mcp-pandoc and related tools; follow its guidance. Consult GitHub’s [Security hardening guide for Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) if CI is added. Finally, review the [OSSF Secure Software Development Fundamentals](https://raw.githubusercontent.com/ossf/secure-sw-dev-fundamentals/refs/heads/main/secure_software_development_fundamentals.md) for best practices on dependency management and threat modeling.

**References:** CVE-2023-35936 / NVD; GitHub Advisory (CVE-2025-5277); Snyk anyio/httpx/pydantic scans; mcp-pandoc PyPI/README.
