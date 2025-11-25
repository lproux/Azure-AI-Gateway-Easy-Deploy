# Microsoft MCP Server Standard: Microsoft.ModelContextProtocol.HttpServer

## Overview

The only paved path for building Microsoft Model Context Protocol (MCP) servers is C# using the `Microsoft.ModelContextProtocol.HttpServer` package. While other languages are possible, only this package is supported and recommended for production-grade secure enterprise deployments.

This package provides built-in authentication (Entra ID with MISE), authorization, rate limiting, and telemetry. It is designed for secure, scalable, and observable MCP servers.

### Key capabilities

- Entra ID authentication and authorization, coupled with MISE-powered token validation. Your MCP server is immediately SFI compliant
- Scope-based authorization (OAuth 2.1 alignment)
- Per-user / per-tenant rate limiting
- Protected Resource Metadata (PRM) endpoint
- OpenTelemetry instrumentation hooks
- Opinionated, hardened middleware ordering

> [!NOTE]
> The MCP + MISE adoption guidance (token validation pipeline, Protected Resource Metadata endpoint, authentication handler registration, authorization integration) is implemented automatically when you add this package. You still need to: provide correct `AzureAd` settings, set `ResourceHost`, define required scopes, host behind an approved Microsoft network edge / reverse proxy, and enforce least-privilege scopes.

## Installation

1. Add the following to your `nuget.config`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="EngThrive-MCP" value="https://pkgs.dev.azure.com/msazure/One/_packaging/EngThrive-MCP/nuget/v3/index.json" />
  </packageSources>
</configuration>
```

> [!TIP]
> All Microsoft full time employees have been granted read access and EngThrive-MCP can be added as an upstream to your own feed. The syntax for the upstream is `azure-feed://msazure/One/EngThrive-MCP@Local`.

1. Add the package via the .NET CLI (this pulls the latest available version from the internal feed):

```bash
dotnet add package Microsoft.ModelContextProtocol.HttpServer --prerelease
```

> [!TIP]
> Use `--version` only when pinning for controlled rollout. Prefer floating versions to automatically receive latest preview updates during active development and to ingest security and resilience updates.

> [!NOTE]
> The package is prerelease because some of its dependencies are prerelease. The package itself is fully supported for production use.

## Quick Start

### 1. Configure Services in `Program.cs`

```csharp
using Microsoft.ModelContextProtocol.HttpServer;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddMicrosoftMcpServer(
    builder.Configuration,
    options =>
    {
        options.ResourceHost = "https://your-customer-facing-top-level-domain";
    })
    .WithToolsFromAssembly();

var app = builder.Build();
```

### 2. Configure the Application Pipeline

```csharp
app.UseMicrosoftMcpServer(); // setup global middleware
app.MapMicrosoftMcpServer(); // map endpoint routes
app.Run();
```

### 3. Configure Entra ID in `appsettings.json`

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "your-tenant-id or common or organizations",
    "ClientId": "your-client-id" // this needs to be your dedicated MCP app ID
  }
}
```

> [!NOTE]
> You may need to pre-authorize MCP host applications that will be used with your dedicated API client application. For example, Visual Studio Code (`aebc6443-996d-45c2-90f0-388ff96faa56`) is not currently authorized for use across the Microsoft tenant. To pre-authorize MCP host applications for a third-party app, add them to your API client app registration under the "Manage" -> "Expose an API" section in the Azure Portal.

> [!IMPORTANT]
> **DO NOT** use a production Entra ID application registration for local development or test environments. Create a distinct app registration per environment (Dev, Test, Prod) and per MCP server. Reusing a production app increases blast radius, complicates incident response, and violates the principle of least privilege.

### 4. Define MCP Tools

```csharp
using System.ComponentModel;
using ModelContextProtocol.Server;

namespace YourMCPService; // Replace with your actual namespace

[McpServerToolType]
public class MyTools
{
    [McpServerTool, Description("Get weather information for a location")]
    public async Task<string> GetWeather(
        [Description("City name")] string city,
        [Description("Country code")] string country = "US")
    {
        // Tool implementation
        return $"Weather in {city}, {country}: Sunny, 72°F";
    }
}
```

> [!IMPORTANT]
> The package guarantees that by the time a tool method executes the caller is authenticated and a `ClaimsPrincipal` is available via `IHttpContextAccessor.HttpContext.User`. **You are responsible for enforcing that the principal has the specific scope(s) required for each tool operation.** If you expose multiple scopes, perform a per-call check (manual claim inspection or an authorization policy) before executing sensitive logic.

## Configuration Options

The `MicrosoftMcpServerOptions` contract:

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `SupportedScopes` | IList&lt;string&gt; | Scopes supported (optional, don't alter this unless you are well versed in how scopes are used by the protocol) | api://<ClientId>/.default |
| `MaxRequestsPerMinutePerUser` | int | Rate limit per authenticated user | 100 |
| `ClientId` | string? | Override Entra ID ClientId (falls back to AzureAd:ClientId) | null |
| `TenantId` | string? | Override Entra ID TenantId (falls back to AzureAd:TenantId) | null |
| `AuthorizationServerInstance` | string? | Override authority base (falls back to AzureAd:Instance) | null |
| `ResourceHost` | string? | Public host (audience) for issued tokens | (required) |

### Configuration methods

Inline (lambda):

```csharp
builder.Services.AddMicrosoftMcpServer(builder.Configuration, o =>
{
    o.ResourceHost = "https://api.contoso.com";
    o.SupportedScopes = ["api://<your-client-id>/Contoso.Read", "api://<your-client-id>/Contoso.Write"]; 
    o.MaxRequestsPerMinutePerUser = 200;
});
```

Options pattern:

```csharp
builder.Services.AddMicrosoftMcpServer(builder.Configuration);
builder.Services.Configure<MicrosoftMcpServerOptions>(o =>
{
    o.ResourceHost = "https://api.contoso.com";
    o.SupportedScopes = ["api://<your-client-id>/Contoso.Read", "api://<your-client-id>/Contoso.Write"]; 
});
```

AppSettings binding:

```json
{
  "MicrosoftMcpServer": {
    "ResourceHost": "https://api.contoso.com",
    "SupportedScopes": ["api://<your-client-id>/Contoso.Read", "api://<your-client-id>/Contoso.Write"],
    "MaxRequestsPerMinutePerUser": 300
  }
}
```

```csharp
builder.Services.AddMicrosoftMcpServer(builder.Configuration);
builder.Services.Configure<MicrosoftMcpServerOptions>(builder.Configuration.GetSection("MicrosoftMcpServer"));
```

Layered overrides:

```csharp
builder.Services.AddMicrosoftMcpServer(builder.Configuration, o =>
{
    o.ResourceHost = "https://api.contoso.com";
});

builder.Services.Configure<MicrosoftMcpServerOptions>(o =>
{
    o.MaxRequestsPerMinutePerUser = 500;
});
```

## Security and Hosting Guidance

**All MCP servers must be hosted behind an approved Microsoft network edge / reverse proxy** that provides corporate-standard DDoS mitigation, traffic inspection, and request normalization as defined in the internal DDoS shielding guidance ([Approved proxies and DDoS shielding](https://eng.ms/docs/initiatives/project-standard/standards-categories/sc-networking/ddos/ads/index)).
**DO NOT** attempt to use Microsoft Graph (msgraph) as an MCP edge or generic ingress for other MCP servers. There is a single sanctioned MCP server surface for Microsoft Graph.

> **Azure API Management is NOT recommended** for MCP servers as the public facing endpoint, as it does not provide globally distributed DDoS protection for production scenarios. It is fine to use as an intermediate proxy.

> [!IMPORTANT]
> Each remote MCP server owned by Microsoft requires a **dedicated Entra ID application (AppId)**. **DO NOT** reuse an existing app registration across multiple MCP servers or combine unrelated resource scopes. Create a unique app registration per server, define only the scopes it serves, and ensure tokens are audience-restricted to that AppId. This is mandatory for isolation, auditing, revocation, and least privilege.

Consult the [MCP Security documentation](./building-secure-mcp.md) for more security guidance.

### Deployment isolation (do NOT co-host with existing backends)

Do not deploy an MCP server in the same **process**, **App Service / container**, or **VM scale set** that currently hosts your existing (non-MCP) production APIs or microservices.

> [!IMPORTANT]
> You must isolate remote MCP servers from existing production backends. Co-hosting increases the blast radius of protocol churn, port / connection pressure, and evolving resource profiles, and can cause collateral outages of stable services.

Rationale:

1. Protocol churn: The MCP protocol and server implementation will iterate rapidly over the coming months (feature evolution, transport improvements, reliability changes). These updates can introduce new dependencies, configuration changes, and transient instability unsuitable for tightly coupled legacy workloads.
2. Connection model: The current non-stateless transport maintains persistent HTTP connections per active session. High parallel session counts can drive elevated ephemeral port consumption and socket state buildup. Co-resident services risk port exhaustion or increased latency under surge conditions.
3. Resource volatility: Model integration and tool orchestration patterns can change CPU, memory, and thread utilization characteristics across versions. Spikes (e.g., burst tool fan‑out) should not starve critical production request threads of unrelated services.
4. Deployment cadence: MCP servers may require faster patch cadence (security, capability enablement). Independent deployment units (separate service, slot, or workload) allow safe progressive rollout without forcing accelerated deployments of unrelated services.
5. Fault isolation: An MCP server experiencing load shedding, circuit breaking, or OOM events must not cascade failures into unrelated API surfaces.

Recommended patterns:

- Host each remote MCP server as a dedicated service (separate app registration + separate deployment unit / microservice).
- Use distinct scaling policies (HPA / autoscale rules) tuned to MCP session + tool invocation metrics, not legacy request patterns.
- Apply independent Safe Deployment rings (canary -> flight -> broad) before broad exposure to internal clients.
- Allocate a separate outbound SNAT / NAT pool if the platform allows, to prevent ephemeral port contention (especially in Azure regions with shared SNAT limits).
- Monitor connection counts (`CURRENT ESTABLISHED`, TIME_WAIT), socket exhaustion warnings, and per-pod/instance thread pool starvation separately from existing APIs.

## Advanced Scenarios

### Custom transport

```csharp
builder.Services.AddMicrosoftMcpServer(builder.Configuration, o =>
{
  o.ResourceHost = "https://api.contoso.com";
})
.WithHttpTransport(t =>
{
  t.Stateless = true; // enable stateless session features
});
```

> [!WARNING]
> Enabling `Stateless` mode removes server-maintained conversational state. You lose: elicitation, sampling, and any server-initiated notifications (e.g., tool change push notifications)

### Extending authentication (MISE options)

```csharp
builder.Services.Configure<MiseOptions>(mise =>
{
  // Example: add custom protocol settings if required
  // mise.AzureAd.Protocols.Add("Custom", new ProtocolOptions { /* ... */ });
});
```

> [!TIP]
> For full MISE configuration surface (advanced client credential sources, protocol tuning, logging, token validation extensibility) review the internal [MISE Configuration Reference](https://eng.ms/cid/3a97a3e5-52f6-46e4-811b-61b172cc679c/fid/f153cc5185322c10be2f69244a198b3e2778cd9293520c7958b71a37b12d357a). Apply only the minimal required settings; avoid over-specifying defaults to preserve forward compatibility.

### Additional authorization policies

```csharp
builder.Services.AddAuthorization(o =>
  o.AddPolicy("Admins", p => p.RequireRole("Administrator")));

app.UseMicrosoftMcpServer();
app.MapMicrosoftMcpServer().RequireAuthorization("Admins");
```

### Dependency injection in tools

```csharp
using System.ComponentModel;
using ModelContextProtocol.Server;

namespace YourMCPService; // Replace with your actual namespace

[McpServerToolType]
public class SecureTools(IHttpContextAccessor accessor)
{
  [McpServerTool, Description("Returns the Entra object id of the current signed in user")]
  public string WhoAmI()
  {
    var user = accessor.HttpContext?.User;
    var oid = user?.FindFirst("oid")?.Value;
    return $"User OID: {oid}";
  }
}
```

### Calling a protected downstream API from a tool

In many MCP scenarios your tool needs to call an internal or external downstream API on behalf of the signed-in caller while preserving user identity and enforcing least-privilege scopes. Use the Microsoft Identity Abstractions `IAuthorizationHeaderProvider` to acquire per-request user tokens and attach them via a typed/ named `HttpClient` plus a delegating handler.

#### 1. Implement a delegating handler to add the user token

```csharp
using System.Net.Http.Headers;
using Microsoft.Identity.Abstractions;

namespace YourMCPService;

/// <summary>
/// Delegating handler that adds authorization headers to outgoing HTTP requests
/// using the Microsoft Identity platform authorization header provider.
/// </summary>
internal sealed class DownstreamAuthorizationDelegatingHandler(
  IAuthorizationHeaderProvider authorizationHeaderProvider
) : DelegatingHandler
{
  // Replace with the scope(s) exposed by the downstream protected API (resource-specific)
  private readonly string[] _scopes = ["api://downstream-app-id/Downstream.Read"];

  protected override async Task<HttpResponseMessage> SendAsync(
    HttpRequestMessage request,
    CancellationToken cancellationToken
  )
  {
    // Acquire an authorization header for the current user
    string authorizationHeader = await authorizationHeaderProvider.CreateAuthorizationHeaderAsync(
      _scopes,
      cancellationToken: cancellationToken);

    if (!string.IsNullOrEmpty(authorizationHeader))
    {
      request.Headers.Authorization = AuthenticationHeaderValue.Parse(authorizationHeader);
    }

    return await base.SendAsync(request, cancellationToken);
  }
}
```

#### 2. Register the handler and named client

Add this during service registration (before building the app):

```csharp
services
  .AddScoped<DownstreamAuthorizationDelegatingHandler>()
  .AddHttpClient(
    "YourDownstreamClient",
    client =>
    {
      client.BaseAddress = new Uri("https://your-downstream-uri");
    })
  .AddHttpMessageHandler<DownstreamAuthorizationDelegatingHandler>();
```

#### 3. Inject and use the client inside a tool

```csharp
using System.ComponentModel;
using ModelContextProtocol.Server;

namespace YourMCPService;

[McpServerToolType]
public class DownstreamTools(IHttpClientFactory httpClientFactory)
{
  [McpServerTool, Description("Get downstream resource status")]
  public async Task<string> GetDownstreamStatus(CancellationToken cancellationToken)
  {
    var client = httpClientFactory.CreateClient("YourDownstreamClient");
    using var response = await client.GetAsync("/status", cancellationToken);
    if (!response.IsSuccessStatusCode)
    {
      return $"Downstream error: {(int)response.StatusCode} {response.ReasonPhrase}";
    }
    return await response.Content.ReadAsStringAsync(cancellationToken); // Consider parsing / validating before returning
  }
}
```

> [!WARNING]
> Do not cache user tokens outside the handler. Always acquire per-request via `IAuthorizationHeaderProvider` to ensure revocation, conditional access, and MFA claims are honored. Avoid broad catch-all scopes (like `user_impersonation`).

### 4. Configure Client Credentials for Downstream Calls

Correct client credential configuration is required for the `DownstreamAuthorizationDelegatingHandler` to successfully perform token acquisition when calling protected downstream APIs. You **must** supply one (or more) supported client credential sources depending on the hosting environment.

> [!NOTE]
> `DownstreamAuthorizationDelegatingHandler` requires `Microsoft.ModelContextProtocol.HttpServer` version **0.1.0-preview.14 or later**. Upgrade if you are on an earlier version.

#### Non-Kubernetes (VM / App Service / Container Apps) – Use Managed Identity

Prefer a user-assigned managed identity (UAMI) for production. The managed identity issues a signed client assertion automatically (no secrets). Configure `AzureAd:ClientCredentials` with `SignedAssertionFromManagedIdentity`.

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "your-tenant-id",
    "ClientId": "your-client-id", // MCP app (resource) ID
    "ClientCredentials": [
      {
        "SourceType": "SignedAssertionFromManagedIdentity",
        "ManagedIdentityClientId": "your-managed-identity-client-id" // user-assigned MI client ID
      }
    ]
  }
}
```

#### Kubernetes (AKS / Arc) – Use Workload Identity (Federated Token File)

Enable Microsoft Entra Workload Identity so a projected service account token (OIDC) is injected. The platform sets `AZURE_FEDERATED_TOKEN_FILE` to the token path. Configure a `SignedAssertionFilePath` credential; if you omit `SignedAssertionFileDiskPath` the library resolves the path from `AZURE_FEDERATED_TOKEN_FILE`.

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "your-tenant-id",
    "ClientId": "your-client-id",
    "ClientCredentials": [
      {
        "SourceType": "SignedAssertionFilePath"
        // If SignedAssertionFileDiskPath is not provided the content of the
        // AZURE_FEDERATED_TOKEN_FILE environment variable is used automatically.
        // "SignedAssertionFileDiskPath": "/var/run/secrets/azure/tokens/oidc-token"
      }
    ]
  }
}
```

> [!TIP]
> Many different k8s hosting platforms internally have different guidance on how to set this up. Consult your local platform docs before reaching out centrally. It is possible to use workload identity for both 3p and 1p apps.

Validation checklist (Kubernetes):

- ServiceAccount annotated with `azure.workload.identity/client-id: <user-assigned-managed-identity-client-id>`.
- Federated identity credential created (issuer, subject `system:serviceaccount:<namespace>:<serviceaccount>`, audience `api://AzureADTokenExchange`).
- Pod environment contains `AZURE_FEDERATED_TOKEN_FILE`.
- `ClientId` matches the MCP app registration (resource) ID.

> [!NOTE]
> **DO NOT** hardcode the token file path unless you have a non-standard projection. Allowing the default to read `AZURE_FEDERATED_TOKEN_FILE` reduces configuration drift.

#### Local Development – Use a Certificate from Key Vault

For local developer machines (where managed identity / workload identity is absent), use a certificate-based credential stored in an Azure Key Vault. This avoids embedding client secrets in source.

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "your-tenant-id",
    "ClientId": "your-client-id",
    "ClientCredentials": [
      {
        "SourceType": "KeyVault",
        "KeyVaultUrl": "https://<your-vault>.vault.azure.net/",
        "KeyVaultCertificateName": "<your-cert-name>"
      }
    ]
  }
}
```

### Observability

Logs and metrics are instrumented via open telemetry. You will have to customize OTEL exporters as you see fit. [View more info about OpenTelemetry at Microsoft](https://eng.ms/cid/8d2e8ca0-cf08-40d3-ba4b-07c3bf8d171a/fid/f45adab6055d46d5dedfce9afc772cafad3a3f38d8bdf71794247fbbb017ada2).

### Session Affinity vs Stateless Mode

MCP conversations frequently rely on a stable server-side context keyed by `Mcp-Session-Id`. You must ensure that successive requests for the same session reach a replica that can decrypt and validate this session identifier.

> [!IMPORTANT]
> Preferred: **edge / load balancer header-based routing** using the `Mcp-Session-Id` header to maintain session affinity. Alternative (fallback): enable stateless mode (`WithHttpTransport(t => t.Stateless = true)`) **AND** persist Data Protection keys. If you enable stateless mode without shared keys across replicas, cross-replica requests for the same session will fail (cannot decrypt session).

Recommended decision order:

1. Use header-based routing (Azure Front Door rules engine or equivalent) to hash on `Mcp-Session-Id`.
2. If not possible (infrastructure constraint), enable stateless mode and back the ASP.NET Core Data Protection key ring with a shared durable store + key encryption.

#### Persisting Data Protection Keys

Example configuration (Azure Blob Storage + Key Vault):

```csharp
services
  .AddDataProtection()
  .SetApplicationName("McpService")
  .SetDefaultKeyLifetime(TimeSpan.FromDays(30))
  .PersistKeysToAzureBlobStorage(
    new Uri(storageAccountUri),
    credential // TokenCredential (Managed Identity / Workload Identity)
  )
  .ProtectKeysWithAzureKeyVault(new Uri(keyVaultUri), credential);
```

Key guidance:

- Use a unique `ApplicationName` per logical MCP service (prod vs staging separated).
- Ensure all replicas (all regions in active-active) share the same key store and vault to prevent decryption failures after failover.
- Rotate keys on the defined schedule; shorter lifetimes increase cryptographic agility but raise re-encryption overhead.
- Monitor key ring health (creation, activation, expiration) via logs.

For full Data Protection configuration details (key storage, encryption at rest, key lifetime strategy) see the official ASP.NET Core guidance: [ASP.NET Core Data Protection configuration](https://learn.microsoft.com/aspnet/core/security/data-protection/configuration/overview?view=aspnetcore-9.0)

#### Validation Checklist

- Load balancer rule routes identical `Mcp-Session-Id` to same backend OR stateless + shared keys configured.
- Data Protection keys are persisted and replicated.
- Key Vault access policies / RBAC grant get, unwrap, wrap permissions to service principal / managed identity.
- Chaos test cross-replica session continuity before production rollout.
- If running stateless: confirmed elicitation, sampling, and server-initiated notification features are NOT required or are reimplemented via an external durable context + push channel.

## Further Reading

- [ModelContextProtocol base package](https://www.nuget.org/packages/ModelContextProtocol)
- [Building secure remote MCP servers](./building-secure-mcp.md)

## Getting help

For additional questions, please start a thread in [MCP Remote and Auth Servers](https://teams.microsoft.com/l/channel/19%3A7a9c6b72646d4f9f9c4abf931a08b88a%40thread.tacv2/MCP%20Security?groupId=f0862597-cf3d-4ec7-beee-1c025c558363&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47).
