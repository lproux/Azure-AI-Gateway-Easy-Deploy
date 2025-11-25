# Building Secure Model Context Protocol (MCP) Servers

> [!IMPORTANT]
> Update (August 2025)
>
> The security baseline for MCP servers has changed:
>
> 1. The only paved path for production-grade MCP servers is C# with the [Microsoft.ModelContextProtocol.HttpServer](./mcp-httpserver.md) package.
> 2. All MCP servers **MUST** be hosted behind an **approved Microsoft network edge / reverse proxy** that provides DDoS mitigation and traffic normalization per the internal Approved DDoS Shielding standard (see [Approved proxies and DDoS shielding guidance](https://eng.ms/docs/initiatives/project-standard/standards-categories/sc-networking/ddos/ads/index)).
> 3. The MCP + MISE adoption guidance is largely implemented automatically when you use the Microsoft.ModelContextProtocol.HttpServer package (token validation pipeline, authentication handler registration, Protected Resource Metadata endpoint). You still need to: supply correct `AzureAd` configuration, define required scopes, set `ResourceHost`, and place the service behind an approved proxy described in the internal DDoS shielding guidance.

This guide outlines essential security considerations and best practices for developing secure MCP servers, based on the [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) and [Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). While it's not required to read the MCP specifications to build secure MCP servers, we highly encourage familiarizing yourself with the core concepts.

## Overview

Security is _paramount_ when building MCP servers, especially those that handle sensitive user data or provide access to protected downstream resources. This guide covers both transport-level security and application-level security considerations to help you build robust, secure MCP implementations.

This guidance is applicable to both **internal-facing** and **external-facing** servers.

## Core security principles

### Defense in depth

Just like with any API or client application, implement multiple layers of security controls rather than relying on a single security mechanism. This includes transport security, authentication, authorization, input validation, and logging. Do not assume that just because your server is not easily discoverable or was only shared with a few people that it won't be abused.

### Principle of least privilege

Grant the minimum necessary permissions required for functionality. Access tokens should be scoped appropriately, and MCP servers should validate that they only accept tokens issued specifically for them. Always follow your project's, team's, and organization's security best practices. Where appropriate, consult with the [Microsoft Security documentation](https://eng.ms/docs/microsoft-security).

### Secure by default

Design your MCP server to be secure out of the box, requiring explicit configuration to reduce security rather than to enable it. Do not expect that the users will take proper precautions to only send the right inputs or in the right format.

## Transport-level security

### HTTP transport requirements

> [!IMPORTANT]
> All HTTP-based MCP servers **MUST** be hosted behind an approved Microsoft network edge / reverse proxy as defined in the internal DDoS shielding guidance ([Approved proxies and DDoS shielding](https://eng.ms/docs/initiatives/project-standard/standards-categories/sc-networking/ddos/ads/index)). Do **NOT** front MCP servers directly on the public internet without an approved network edge in front of it. Do **NOT** attempt to use Microsoft Graph (msgraph) itself as an MCP network edge or generic front door for arbitrary MCP servers. There is a single sanctioned MCP server surface for Microsoft Graph.

> [!IMPORTANT]
> Each remote MCP server **MUST** have its own dedicated Entra ID application (AppId). Do not reuse a single app registration for multiple servers. Define only the scopes specific for that server, and enforce audience (resource) validation so that tokens issued for one server cannot be replayed against another. You **MUST NOT** pass tokens through that were not issued for your MCP server.

For C# servers, you **MUST** use the [Microsoft.ModelContextProtocol.HttpServer](./mcp-httpserver.md) package, which provides built-in authentication, authorization, rate limiting, and telemetry. See [mcp-httpserver.md](./mcp-httpserver.md) for a full tutorial and production checklist.

HTTP-based MCP servers are effectively web APIs, so the security threat model, as well as general conventions that are applicable to building web APIs at Microsoft are broadly applicable here as well. When implementing HTTP-based MCP servers:

- **All endpoints MUST use HTTPS** in production environments.
- Access tokens **MUST** be sent via the `Authorization` header:

  ```http
  Authorization: Bearer <access-token>
  ```

- **NEVER** pass tokens through URI query strings or request bodies.
- **NEVER** pass tokens to the MCP server that were not issued for said MCP server.
- If using Entra ID authentication, you **MUST** use [MISE](https://aka.ms/mise/1p) for token acquisition and validation.
- Unless otherwise necessary for business reasons (e.g., GitHub, LinkedIn), you **MUST** use Entra ID for authentication and authorization.

> [!IMPORTANT]
> Refer to the internal [MCP + MISE adoption guide](https://eng.ms/docs/microsoft-security/identity/app-plat-and-graph/app-vertical/aad-first-party-apps/identity-platform-and-access-management/microsoft-identity-platform/secure-mcp-servers) for details.

### STDIO transport security

STDIO-based MCP servers are effectively **local binaries** that run on the user's machine. For STDIO-based MCP servers:

- **DO NOT** rely on environment variables for passing credentials **UNLESS** you are using API keys.
- **DO** use established libraries, like [Microsoft Authentication Library (MSAL)](https://msal.dev) or [OneAuth](https://aka.ms/oneauth), to acquire tokens when implementing client authentication with Entra ID.
- For non-Entra ID OAuth flows, use the [MCP C# SDK](https://github.com/modelcontextprotocol/csharp-sdk) or one of the [official MCP SDKs](https://modelcontextprotocol.io/introduction).
- **DO NOT** implement the authentication process from scratch.
- **DO NOT** assume that authorization decisions are made client-side.
- **ALWAYS** assume that the connecting client can be malicious and threat model accordingly.

## Authentication and authorization

### OAuth 2.1 implementation

To be compliant with the MCP specification, your server **MUST** support [RFC 9728](https://datatracker.ietf.org/doc/html/rfc9728) for Protected Resource Metadata (PRM). If you are using any of the official MCP SDKs, this functionality is available out-of-the-box and you do not need to configure it manually.

The PRM document is the "business card" of the MCP server that outlines the authorization server used (e.g., Entra ID URI), scopes used, as well as how tokens are sent to the server.

Additionally, to be broadly adoptable by _any_ spec-compliant MCP client, your MCP server **SHOULD** support [RFC 7591](https://datatracker.ietf.org/doc/html/rfc7591/) Dynamic Client Registration. Entra ID and GitHub do not support it out-of-the-box, therefore additional work will be needed to implement it directly.

### Token validation

Your server **MUST** validate all inbound tokens. Use [MISE](https://aka.ms/mise/1p) to ensure that all tokens that are sent to the MCP server were **issued for the MCP server**. Refer to [MCP + MISE adoption guide](https://eng.ms/docs/microsoft-security/identity/app-plat-and-graph/app-vertical/aad-first-party-apps/identity-platform-and-access-management/microsoft-identity-platform/secure-mcp-servers) for implementation details.

This also means that token passthrough (e.g., acquiring a token for Microsoft Graph and then passing it directly to your MCP server when the token's destination is Microsoft Graph) is **strictly prohibited**. This is an anti-pattern that breaks security boundary conventions, and that also means that your token cannot be properly validated on the MCP server.

## Implementation best practices

### Error handling best practices

Return appropriate HTTP status codes:

- **401 Unauthorized**: Missing or invalid token
- **403 Forbidden**: Valid token but insufficient permissions
- **400 Bad Request**: Malformed authorization request

>[!NOTE]
>There is currently [a proposal](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/835) in the works that will help establish incremental consent patterns through `WWW-Authenticate`.

### Logging and monitoring

- Log all authentication and authorization events
- Monitor for unusual access patterns
- Implement rate limiting
- Log security events without exposing sensitive data

### Secrets management

- Store secrets securely ([Azure Key Vault](https://learn.microsoft.com/azure/key-vault/general/basic-concepts)) and do not embed them in MCP server code
- Never log or expose secrets in error messages
- Never expose secrets in LLM responses/context

## Additional resources

- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)
- [OAuth 2.1 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)
- [OAuth 2.1 Draft Specification](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13)
- [STRIKE Community (internal)](https://strikecommunity.azurewebsites.net/)

## Getting help

For additional questions, please start a thread in [MCP Security](https://teams.microsoft.com/l/channel/19%3A7a9c6b72646d4f9f9c4abf931a08b88a%40thread.tacv2/MCP%20Security?groupId=f0862597-cf3d-4ec7-beee-1c025c558363&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47).
