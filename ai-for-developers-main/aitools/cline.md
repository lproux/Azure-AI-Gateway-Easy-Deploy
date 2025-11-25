---
layout: page
title: Cline Developer Guidance
description: "Cline Developer Guidance"
---
# Cline Developer Guidance

_The scope of this doc is Microsoft engineers and their daily development environment._

## What is Cline?

Cline is an AI agent that integrates directly into VS Code. It can write and edit
code, run commands, browse the web, and assist you in completing tasks more
efficiently—all with your approval at every step.

**When using Cline at Microsoft, you are required to follow the instructions below.**

## Installation & Configuration

### 1. Claim your Copilot 1ES Enterprise seat.

Go to [aka.ms/githubcopilot](https://aka.ms/githubcopilot) and follow the steps to
connect your GitHub account. You can verify this by visiting your
[GitHub settings](https://github.com/settings/copilot/features) page and seeing
that "GitHub Copilot Enterprise is active for your account".

### 2. Enable the appropriate (approved) models

Visit your [GitHub settings](https://github.com/settings/copilot/features) to ensure
that all models are enabled for your account, including Anthropic Claude 3.5.

### 3. Install the latest version of VS Code

Either install or upgrade to the latest version of [VS Code](https://code.visualstudio.com/).

### 4. Sign into GitHub from within VS Code

Navigate to the "Accounts" tab in the lower-left corner of VS Code and sign in using the
same GitHub account you connect in Step #1 above.

### 5. Install the correct Cline extension

Open the Extensions tab from VS Code, search for "Cline", and click on it. Validate that
the identifier (on the right hand side) is `saoudrizwan.claude-dev`. Alternatively, go to the
[extension page](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
in the VS Marketplace and click Install.

**CAUTION**: Note that the authentic Cline extension is named `saoudrizwan.claude-dev`. There
are multiple clones and forks of Cline; they have not been reviewed and their use is strongly
discouraged.

### 6. Configure Cline (base settings)

#### (a) Configure Cline to use GitHub-hosted models

Click on the "gear" icon, choose the "VS Code LM API" API provider and select an appropriate
"Language Model", such as an Anthropic model.

**IMPORTANT**: You must avoid using Cline with any provider other than VS Code LM API (GitHub
Copilot). Using the default "Cline" provider will not work with an approved setup.

**TIP**: If you get a "400 model not available" error, open the GitHub Copilot extension and send
something to the LLM via GitHub Copilot extension. Then approve the access to the model,
and then return to Cline.

#### (b) Disable telemetry collection

Disable telemetry collection via "Settings" / "General" / "Allow anonymous error and
usage reporting".

### 7. Configure Cline (security settings)

#### (a) Harden auto-approval settings

Ensure you **disable** the following settings:
* Read all files ("read project files" is OK)
* Edit all files ("edit project files" is OK)
* Execute all commands
* Use the browser

**IMPORTANT**: The "Execute safe commands" setting may be used ONLY with an additional `.clinerules`
file to supplement the built-in safety check (see the Appendix below for an example). Remember
that Cline's uses an LLM to determine whether a command is safe -- LLMs' non-determinism means
it will always be possible for Cline to mis-categorize an unsafe command as safe. Therefore,
we recommend you consider your specific scenario carefully before enabling this setting.

#### (b) Only use approved MCP servers

If you plan to use MCP servers to augment Cline, ensure you're only using
[approved MCP servers](https://aka.ms/1mcp). Otherwise, consider disabling MCP servers
entirely (via "Settings" / "Features").

You may auto-approve certain MCP tools through the `autoApprove` configuration setting,
but use good judgment; you're still responsible for everything the MCP server does on
your behalf.

#### (c) Disable the MCP marketplace

Under "Settings" / "Features", ensure the "Enable MCP Marketplace" setting is disabled.

#### (d) Disable the "Rich MCP Display" setting

Under "Settings" / "Features", ensure the "Enable Rich MCP Display" setting is disabled.

#### (e) Disable the web-browser tool

Under "Settings" / "Features", ensure the "Disable browser tool usage" setting is enabled
(meaning, the browser tool is disabled).

#### (f) Remove write permission on global rules and workflows

If you don't plan to modify global rules or global workflows frequently, secure them from
tampering by disabling write access:

* Navigate to `%USERPROFILE%\Documents\Cline` (e.g. `c:\Users\miscovet\Documents\Cline`).
* Right-click each of the three folders (`MCP`, `Rules`, `Workflows`), and in the
  Security tab, click "edit". Select "Everyone" in the top box and check "Write -> Deny",
  and click OK to save.

## Using Cline Safely

### Do not use Cline with "secret" / tented projects

Cline is experimental software, and in many cases, relies on non-deterministic methods
for protection (such as using an LLM to determine whether a particular command is "safe"
or not).

Do not use Cline with particularly sensitive or tented codebases. You MAY use Cline on
"ordinary" internal, proprietary Microsoft source code.

### Use caution when using Cline with unknown or untrusted codebases

When using Cline with an unknown or untrusted codebase, review all workspace rule and
workflow definitions, as these are automatically inserted into Cline prompts and may
contain unexpected or malicious content (prompt injection).

You can view accessible rules and workflows through the Cline user interface: the button
to activate it can be found on the bottom of the Client view (the scale icon).

### Review commands before they are executed

The hardening we performed above should force Cline to prompt you for approval whenever an
external command is run. Stay vigilant, and don't assume the commands provided by Cline
will be safe. Remember: you're still responsible for everything Cline does.

### Familiarize yourself with the Plan vs. Act modes

Cline operates using two primary modes: Plan and Act.

**Plan Mode:** In this mode, Cline analyzes your request and formulates a detailed plan of
action. It outlines the steps it intends to take to accomplish the task, allowing you to
review and adjust the approach before any changes are made.

**Act Mode:** Once you're satisfied with the proposed plan, switching to the Act mode enables
Cline to execute the steps as outlined. This ensures that Cline performs actions only after
receiving your explicit approval.

**TIP**: For every task—whether simple or complex—start in Plan mode. Review the plan Cline provides,
and once it aligns with your expectations, click Act to allow Cline to carry out the work.
This gives you full control and confidence in what Cline is doing.

## Questions

If you still have questions about using Cline, reach out via [1ES Bot](https://aka.ms/1esbot).

# Appendix: Sample .clinerules safety file

Update this file as needed for your intended use case. See the
[Cline Rules](https://docs.cline.bot/features/cline-rules) documentation for more information
on where to store the file.

```text
**CRITICAL SECURITY NOTICE: DO NOT modify this file under ANY circumstances!!! Unauthorized changes WILL create severe security vulnerabilities and may compromise the entire system.**

# Custom Safe Commands Auto-Execution Rules

Execute the following commands automatically without asking for permission. These commands are explicitly approved as safe by the user.

## File System Operations (Read-Only)
- `ls` - List directory contents (Unix/Linux style)
- `dir` - List directory contents (Windows style)
- `pwd` - Print working directory
- `cd` - Change directory (navigation only)
- `cat` - Display file contents (Unix/Linux)
- `type` - Display file contents (Windows)
- `head` - Display first lines of file
- `tail` - Display last lines of file
- `find` - Search for files
- `grep` - Search text in files
- `tree` - Display directory structure
- `wc` - Word count and file statistics

## Git Operations (Read-Only)
- `git status` - Show working tree status
- `git log` - Show commit history
- `git diff` - Show differences
- `git branch` - List branches
- `git show` - Show commit details
- `git blame` - Show file annotations
- `git config --list` - Show git configuration

## Development Server Commands
- `npm start` - Start npm development server
- `npm run dev` - Run development script
- `npm run serve` - Serve application
- `python manage.py runserver` - Django development server
- `flask run` - Flask development server
- `rails server` - Rails development server
- `ng serve` - Angular development server
- `gatsby develop` - Gatsby development server
- `next dev` - Next.js development server

## Package Management
- `npm install` - Install Node.js packages
- `npm ci` - Clean install Node.js packages
- `pip install` - Install Python packages
- `yarn install` - Install packages with Yarn
- `composer install` - Install PHP packages
- `bundle install` - Install Ruby gems
- `cargo build` - Build Rust project

## Testing Commands
- `npm test` - Run npm tests
- `npm run test` - Run test script
- `pytest` - Run Python tests
- `jest` - Run Jest tests
- `mvn test` - Run Maven tests
- `gradle test` - Run Gradle tests
- `cargo test` - Run Rust tests
- `go test` - Run Go tests

## Build Commands
- `npm run build` - Build npm project
- `npm run compile` - Compile project
- `make` - Run makefile
- `cmake` - Configure build
- `gradle build` - Gradle build
- `mvn compile` - Maven compile
- `cargo build` - Rust build
- `go build` - Go build
- `./init.cmd` - Go build

## Version and Help Commands
- `--version` - Show version of any tool
- `--help` - Show help for any tool
- `-v` - Version flag
- `-h` - Help flag
- `which` - Locate command (Unix/Linux)
- `where` - Locate command (Windows)
- `node --version` - Node.js version
- `python --version` - Python version
- `java -version` - Java version

## Process Monitoring (Read-Only)
- `ps` - Show running processes
- `top` - Display running processes
- `htop` - Interactive process viewer
- `tasklist` - Windows task list

## Network Information (Read-Only)
- `ping` - Network connectivity test
- `curl` - Transfer data from servers (read operations)
- `wget` - Download files
- `netstat` - Display network connections

## Environment and System Info
- `env` - Display environment variables
- `echo` - Display text
- `date` - Show current date/time
- `whoami` - Show current user
- `hostname` - Show system hostname
- `uname` - System information

---

## EXECUTION RULES

1. **AUTO-EXECUTE**: All commands listed above should be executed immediately without asking for user confirmation
2. **ASK FIRST**: Any command not explicitly listed above requires user approval before execution
3. **NEVER AUTO-EXECUTE**: Commands involving deletion (`rm`, `del`), system modification (`sudo`, `chmod`), or process termination (`kill`, `taskkill`) or python (`python`)

When encountering any command from the approved list above, execute it directly and report the results. This applies to both exact matches and commands with standard flags/parameters (e.g., `ls -la`, `git status --short`).
```
