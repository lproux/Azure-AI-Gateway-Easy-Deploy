# Changelog

This page will track any major updates or changes to the content on aka.ms/1mcp.

# 2025-09-23
- Added new requests for local and remote servers received by 9/23 to the 1mcp list in [MCP servers at Microsoft](./index.md). Remote servers are tagged with `add to registry` for entry into the API Center:

Added to "Official servers for internal use" (1P):

- CodeTesting — Private preview
- dotnet-agent — Private preview

Added to "3P MCP Servers › In-review servers":

- Serena — Local server
- ESLint MCP — Local server
- Filesystem — Local server

## 2025-09-16

- Expanded `mcp-httpserver.md` with guidance for pre-authorizing MCP host applications (e.g., VS Code client) in Entra ID app registrations.
- Updated `MicrosoftMcpServerOptions` description: `SupportedScopes` now optional with default `api://{ClientId}/.default`.
- Revised scope examples to fully qualified `api://<your-client-id>/...` patterns.
- Added MISE configuration TIP linking to the internal MISE Configuration Reference.
- Introduced comprehensive section on configuring client credentials for On-Behalf-Of downstream API calls (Managed Identity, Workload Identity, Key Vault certificate).

## 2025-08-29

- Added new local server publishing requirements in [Publishing an MCP server](./publishing-an-mcp-server.md#publishing-steps)

## 2025-08-27

- New paved path: `mcp-httpserver.md` introduces `Microsoft.ModelContextProtocol.HttpServer` as the standard C# remote MCP server package.
- Hosting change: require AFD, Dataplane, or AD Gateway; Azure API Management removed.
- Security doc updated: adoption steps automated by package

## 2025-08-21

- Modified instructions for registry URL usage in VS Code to be direct API Center link rather than redirect due to a bug with VS Code handling redirects as the registry link.
- Added new requests for local and remote servers received by 8/21 4PM PST to the 1mcp list in [MCP servers at Microsoft](./index.md). Remote servers are tagged with `add to registry` for entry into the API Center:

Added to "Official servers for internal use" (1P):

- Bing PerfPipeline MCP Server — Private preview
- Debug Analysis — Under development
- IcM — Private preview
- Rush MCP — Generally available
- SubstrateMCP — Private preview
- Ask ES Chat — Generally available

Added to "3P MCP Servers › In-review servers":

- DeepWiki — Remote server
- Filesystem — Local server
- MCP-Memory — Local server
- mcp-mermaid — Local server
- Sequential Thinking — Local server
- SonarQube — Local server
