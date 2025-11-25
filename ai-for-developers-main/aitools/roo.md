---
layout: page
title: Roo Developer Guidance
description: "Roo Developer Guidance"
---
# Roo / MS Roo Developer Guidance

_The scope of this doc is Microsoft engineers and their daily development environment._

**This document covers both Roo ([Roo Code](https://github.com/RooCodeInc/Roo-Code)) and
[Microsoft's fork of Roo](https://github.com/ai-microsoft/Roo-Cline).**

## What is Roo?

Roo is an AI coding tool that integrates directly into VS Code. It can write and edit
code, run commands, browse the web, and assist you in completing tasks more
efficiently.

**When using Roo at Microsoft, you are required to follow the instructions below.**

## Installation & Configuration

### 1. Claim your Copilot 1ES Enterprise seat.

Go to [aka.ms/githubcopilot](https://aka.ms/githubcopilot) and follow the steps to
connect your GitHub account. You can verify this by visiting your
[GitHub settings](https://github.com/settings/copilot/features) page and seeing
that "GitHub Copilot Enterprise is active for your account".

### 2. Enable the appropriate (approved) models

Visit your [GitHub settings](https://github.com/settings/copilot/features) to ensure
that all models are enabled for your account, including Anthropic Claude.

### 3. Install the latest version of VS Code

Either install or upgrade to the latest version of [VS Code](https://code.visualstudio.com/).

### 4. Sign into GitHub from within VS Code

Navigate to the "Accounts" tab in the lower-left corner of VS Code and sign in using the
same GitHub account you connect in Step #1 above.

### 5. Install the correct Roo extension

#### To install the private (MS Roo) extension

Navigate to the [private repository](https://github.com/ai-microsoft/ai-coder-tools/blob/main/ts-server/README.md#all-in-one-installation)
and follow the instructions to download and run the `AllInOne.ps1` installation script.

#### To install the public Roo extension

Open the Extensions tab from VS Code, search for "Roo", and click on it. Validate that
the identifier (on the right hand side) is `rooveterinaryinc.roo-cline`. Alternatively, go to the
[extension page](https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline)
in the VS Marketplace and click Install.

**CAUTION**: Note that the authentic public Roo extension is named `RooVeterinaryInc.roo-cline`. There
are multiple clones and forks of Roo; other than the MS Roo fork, they have not been reviewed and their
use is strongly discouraged.

### 6. Configure Roo (base settings)

#### (a) Configure Roo to use GitHub-hosted models

Click on the "gear" icon, select "Providers", then choose the "VS Code LM API" API provider and select
an appropriate "Language Model", such as an Anthropic model like `copilot - claude-opus-4`.

**IMPORTANT**: You must avoid using Roo with any provider other than VS Code LM API (GitHub
Copilot).

**TIP**: If you get a "400 model not available" error, open the GitHub Copilot extension and send
something to the LLM via GitHub Copilot extension. Then approve the access to the model,
and then return to Roo.

#### (b) Disable telemetry collection

Disable telemetry collection via "Settings" / "About Roo Code" / "Allow anonymous error and
usage reporting".

### 7. Configure Roo (security settings)

#### (a) Harden auto-approval settings

Review the [Roo Code documentation](https://docs.roocode.com/features/auto-approving-actions/) for
more details on auto-approval.

Ensure you **disable** the following settings:
* Read: Read files outside of project workspace
* Write: Write files outside of project workspace
* Write: Include protected files

**IMPORTANT**: Do not enable `*` for "allowed auto-execute commands". You may provide specific commands,
but be wary of [unintended consequences of runaway agents](https://www.businessinsider.com/replit-ceo-apologizes-ai-coding-tool-delete-company-database-2025-7).
Note that by default, a number of commands, including `npm install` are provided in the "safe" list.

#### (b) Only use approved MCP servers

If you plan to use MCP servers to augment Roo, ensure you're only using
[approved MCP servers](https://aka.ms/1mcp). Otherwise, consider disabling MCP servers
entirely (via "..." (top left corner) / "MCP Servers" / "Enable MCP Servers").

You may auto-approve certain MCP tools through the `autoApprove` configuration setting,
but use good judgment; you're still responsible for everything the MCP server does on
your behalf.

#### (c) Disable the web-browser tool

Under "Settings" / "Browser", ensure the "Enable browser tool usage" setting is disabled.

#### (d) Remove write permission on global rules and workflows

If you don't plan to modify global rules or global workflows frequently, secure them from
tampering by disabling write access:

* Navigate to `%USERPROFILE%\.roo` (e.g. `c:\Users\miscovet\.roo`).
* Right-click each of the contained folders (`rules`, `rules-code`, `rules-{mode}`), and in the
  Security tab, click "edit". Select "Everyone" in the top box and check "Write -> Deny",
  and click OK to save.

#### (e) Leverage .rooignore to hide sensitive files from Roo

If you have sensitive files in your local workspace (e.g. `.env`) that Roo should never
examine, you can list them in [.rooignore](https://docs.roocode.com/features/rooignore).

#### (f) Harden codebase indexing

Roo supports codebase indexing with an embedding provider and a Qdrant vector store.
Currently, support for Azure OpenAI is blocked on [#5806](https://github.com/RooCodeInc/Roo-Code/pull/5806),
but a local Ollama model appears to work.

Do not use third-party hosted Qdrant stores. You may use a local Docker container as described
in the [Roo documentation](https://docs.roocode.com/features/codebase-indexing).

## Using Roo Safely

### Do not use Roo with "secret" / tented projects

Roo is experimental software, and in many cases, relies on non-deterministic methods
for protection (such as using an LLM to determine whether a particular command is "safe"
or not).

Do not use Roo with particularly sensitive or tented codebases. You MAY use Roo on
"ordinary" internal, proprietary Microsoft source code.

### Use caution when using Roo with unknown or untrusted codebases

When using Roo with an unknown or untrusted codebase, review all workspace rule and
workflow definitions, as these are automatically inserted into Roo prompts and may
contain unexpected or malicious content (prompt injection).

### Review commands before they are executed

The hardening we performed above should force Roo to prompt you for approval whenever an
external command is run (except for those you specifically permitted). Stay vigilant, and
don't assume the commands provided by Roo will be safe. Remember: you're still responsible
for everything Roo does.

### Familiarize yourself with the Plan vs. Act modes

Roo operates using two primary modes: Plan and Act.

**Plan Mode:** In this mode, Roo analyzes your request and formulates a detailed plan of
action. It outlines the steps it intends to take to accomplish the task, allowing you to
review and adjust the approach before any changes are made.

**Act Mode:** Once you're satisfied with the proposed plan, switching to the Act mode enables
Roo to execute the steps as outlined. This ensures that Roo performs actions only after
receiving your explicit approval.

**TIP**: For every task—whether simple or complex—start in Plan mode. Review the plan Roo provides,
and once it aligns with your expectations, click Act to allow Roo to carry out the work.
This gives you increased confidence in what Roo is doing.

## Questions

If you still have questions about using Roo, reach out via [1ES Bot](https://aka.ms/1esbot).
