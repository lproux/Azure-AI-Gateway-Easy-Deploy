---
layout: page
title: Quick Reference - AI Tools for Microsoft Developers
description: "Quick Reference - AI Tools for Microsoft Developers"
permalink: /
---

# Quick Reference - AI Guidance for Microsoft Developers

## Purpose

This page explains our 1ES, CELA, DSB joint guidance on the use of third party AI tools and models for software development at Microsoft.

## Background

Our developer tools business depends on the success of GitHub Copilot. Our engineers build leading-edge AI by dogfooding AI in their daily engineering flow. Microsoft engineers should dogfood our tools before adopting third party tools for use in development. Our engineers should use first party tools for development in order to protect Microsoft IP and provide feedback. When a Microsoft engineer uses a competitive offering (e.g. Cursor, ChatGPT), we deprive ourselves of valuable telemetry and EngThrive data.

Furthermore, third party tools present a risk of indexing proprietary code, customer code/data, partner code/data, internal business information, and anything that constitutes “Confidential Information” as defined by the Confidential Information Policy (collectively, “Sensitive IP”). In addition, third party tools may output suggestions that violate copyrights and/or open source licenses.

Third-party AI tools should not be used with Microsoft customer data.

Please note that all internal use of third party AI tools, APIs, and models requires review from frontline CELA, Microsoft Procurement (i.e. SSPA), and Microsoft Digital. Non-development use of third party models must meet the requirements in [Checklist for Using Third Party Models](https://docs.opensource.microsoft.com/legal/cela-guidance/checklist-for-using-third-party-models/) and be submitted to the [Third Party AI Models CELA Review tool](https://microsoft.sharepoint.com/sites/AIReviews).

### Generative AI Developer Desktop Tools

| Tool | Use with Sensitive IP | Use w/non-Sensitive IP | Security note |
| --- | --- | --- | --- |
| ChatGPT website & apps | NO | OK | Not security reviewed |
| Claude website | NO | OK | Not security reviewed |
| Cline extension | [Requirements](/aitools/cline.md) | [Requirements](/aitools/cline.md) | See [security notes](/aitools/cline.md) |
| Cursor editor | NO | NO (blocked) | Not security reviewed |
| DeepSeek chat site | NO | NO (blocked) | Not security reviewed |
| Gemini website | NO | OK | Not security reviewed |
| GitHub Copilot | 1ES [Enterprise SKU](https://aka.ms/copilot) | OK | DSR reviewed, 1P GitHub product |
| MCP Servers | Follow [OSS guidance](https://docs.opensource.microsoft.com/using/) <br> <br> See [allowed](https://aka.ms/1mcp) list of MCP servers to use internally | Follow [OSS guidance](https://docs.opensource.microsoft.com/using/) | Refer to guidance |
| Microsoft 365 Copilot (copilot.microsoft.com) | Work SKU only | OK | 1P Microsoft product |
| MS Roo (Roo fork) | [Requirements](/aitools/roo.md) | [Requirements](/aitools/roo.md) | See [security notes](/aitools/roo.md) |
| Roo (Cline fork) | [Requirements](/aitools/roo.md) | [Requirements](/aitools/roo.md) | See [security notes](/aitools/roo.md) |
| Windsurf Editor | NO | OK | Not security reviewed |
| visily website and apps | NO | OK | Not security reviewed |
| locofy.ai Figma plug-in | NO | OK | Not security reviewed |
| [GitHub Spark](https://github.com/spark) - model provider guidance below applies  | NO | OK | 1P Microsoft product |
| Other tools not in list | NO | Use care | Security state varies |

### AI Models & Sensitive IP including Microsoft internal code

To use the pre-approved Claude, Gemini, and Open AI models, simply use the 1ES-provided GitHub Copilot Enterprise product. At this time, the GitHub Models product is not available for use at Microsoft.

| Model Provider | General Use | With GitHub Copilot | Enterprise Model SKUs |
| --- | --- | --- | --- |
| Anthropic Claude | Not approved | OK w/ 1ES [Enterprise SKU](https://aka.ms/copilot) | Requires CELA/SSPA review |
| Google Gemini | Not approved | OK w/ 1ES [Enterprise SKU](https://aka.ms/copilot) | Requires CELA/SSPA review |
| OpenAI | Not approved | OK w/ 1ES [Enterprise SKU](https://aka.ms/copilot) | Requires CELA/SSPA review |

The above tables are for quick reference, please see [details](guidance.md) to get further guidance about these tools as well as non-development usage, local models and tools, usage under enterprise licenses, etc...

We are no longer accepting new asks to be included in this list. 
