# Building and Publishing Microsoft-Developed MCP Servers

Last Edited: September 19, 2025
---

## Official MCP Server Lists

### MCP servers for 3rd-party consumption

**⚠️ Due to non-compliant authentication flows, do NOT publish to the official MCP registry.** New guidance will be provided soon. The [Official (Community) MCP Registry](https://github.com/modelcontextprotocol/registry) is maintained by Anthropic and is a data-only endpoint (no web interface). It will serve as an upstream data source for other MCP registries such as the GitHub MCP Registry. Contact Joel Verhagen (jver@microsoft.com) or Jonathan Giles (jogiles@microsoft.com) if you have questions.

A manually curated list for 3rd-party consumption is published in the [microsoft/mcp](https://github.com/microsoft/mcp/blob/main/README.md) GitHub repository. Create a PR against the `README.md` to list your MCP server.

The GitHub MCP Registry is published at [github.com/mcp](https://github.com/mcp). Submissions are manual for now. Contact Toby Padilla (toby@github.com) if you are interested in listing your server.

Another manually curated list for Azure API Center is published at [mcp.azure.com](https://mcp.azure.com/). For more information see the [Azure/mcp-center](https://github.com/Azure/mcp-center) repository. Contact AzureToolsCatalog@microsoft.com if you have questions.

### MCP servers for 1st-party (internal) consumption

MCP Servers for Microsoft (1st-party) internal consumption are published [here](https://aka.ms/1mcp#access-the-1es-mcp-registry).

If you are aware of an MCP Server that is not on the list, submit a new "[MCP server request](https://aka.ms/MCPServerRequest)" issue on the [1es/ai-for-developers](https://github.com/1es/ai-for-developers) repository to ensure it is included moving forward; refer to the Pre-Publishing Steps section below.

## Publishing an MCP Server

### General MCP server building guidance

- Submit any server intended to be useable by developers at Microsoft, local or remote, to be added to the 1ES MCP registry: [aka.ms/MCPServerRequest](https://aka.ms/MCPServerRequest). The registry is publicly viewable. Do not share any confidental information through metadata. Ensure server-level authentication implemented for your server prior to publishing.

- DO NOT publish your MCP Server to the Anthropic community MCP Registry. The authentication methods are non-compliant and we are working with them to provide secure methods.

- DO NOT build an MCP Server to access resources whose API is owned by another Microsoft team unless the owning team explicitly grants permission. An owning team may deny permission due to some business-related reason.

- DO NOT publish MCP Servers as samples; instead, publish them as official MCP Servers adhering to the guidelines in this document.

- DO NOT provide MCP Servers as sample source code for an application or service. All MCP Servers must follow the guidelines in this document.

- For an Azure-branded MCP Server, DO contact the [Azure-MCP team](https://teams.microsoft.com/l/channel/19%3AQTW6Ai42VjqkZuS0hEsVWYhyXRtZHQ20MZ5KKzQ7ap81%40thread.skype/Azure%20MCP?groupId=3e17dcb0-4257-4a30-b843-77f47f1d4121&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47&ngc=true&allowXTenantAccess=true). They’ll add your MCP Server to the existing [Azure MCP server](https://github.com/Azure/azure-mcp).

- DO implement MCP Servers that do not require access to a client’s local resources, data, or tools, using the [Streamable HTTP Transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http) and host it as an HTTP service. Make sure your service scales well and follows proper authentication practices. Some templates to get you started building an MCP server can be found here: [Awesome Azure Developer CLI](https://azure.github.io/awesome-azd/?tags=mcp).

- DO implement MCP Servers requiring access to a client’s local resources, data, or tools, using the [stdio transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#stdio). It is highly recommended you use .NET and the [Official .NET MCP SDK](https://github.com/modelcontextprotocol/csharp-sdk) and ship it as a [single, self-contained executable file](https://learn.microsoft.com/en-us/dotnet/core/deploying/single-file/overview?tabs=cli). Your MCP Server must not require that customers pre-install any components like language runtimes or docker. If you want to use another language/SDK, please contact [Jeffrey](mailto:jeffreyr@microsoft.com).

> [!IMPORTANT]
> DO use a production-classified pipeline to build and publish your MCP server that extends the 1ES Pipeline Template. For reference, see the [Azure MCP server pipeline implementation](https://github.com/Azure/azure-mcp/tree/main/eng/pipelines/templates).

> [!NOTE]
> To access the following template files, you will use your GHEMU credentials. All FTEs should have access; if you run into difficulty logging in, refer to [the documentation](https://eng.ms/docs/more/github-inside-microsoft/troubleshoot/get-started) maintained by the GitHub inside Microsoft team for troubleshooting steps.

- See this [sample repository](https://github.com/microsoft/mcp-pr/tree/main/Resources#-code-repositories) as a template for your MCP Server’s starting point, depending on which language you're using. This sample covers best practices regarding documentation and support. While all guidance may not be relevant to your use case, follow the structure in the file so all MCP Servers README files are consistent.
    - For remote MCP Servers, include the URL and any authentication requirements.
    - For local MCP Servers, describe how users install, update, and remove the MCP package.

### Pre-Publishing Steps
1. Ensure that you are a member of the [Microsoft GitHub organization](https://github.com/microsoft). If you have access issues, follow [the instructions from the Microsoft Open Source team](https://docs.opensource.microsoft.com/github/opensource/accounts/).
2.	Identify if you plan for your server to be consumed internally, externally or both
    -  If your plan is to release for 3P consumption, refer to the existing [Open Source release guidance](https://docs.opensource.microsoft.com/releasing/) to confirm CELA/OSS compliance needs
3.	Determine if the server will only be hosted locally or also able to be hosted remotely
    -  For remote servers, leverage the [MCP 1P Publishing channel @ Microsoft Teams](https://teams.microsoft.com/l/channel/19%3A618ed13e95e743daafc61b4197d6aada%40thread.tacv2/MCP%201p%20Publishing?groupId=f0862597-cf3d-4ec7-beee-1c025c558363&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47) for additional guidance
4.	Establish a name for the server. There is no enforced naming convention for MCP servers regarding casing or capitalization; however, teams should ensure alignment with branding guidance, as they would for any open-source software released by the company. Consult your CELA representative and follow any applicable legal review processes to confirm appropriate usage.
5.	Refer to [the Microsoft Open Source development guidance](https://docs.opensource.microsoft.com/using/guidance-for-open-source-usage/rebuilding/) for repo creation and pipeline guidance within the ADO project used for the MCP server

> **NOTICE:** The SDL tasks for MCP server compliance are continuously being updated. Any new changes will be highlighted/formatted to easily parse the addition. 

6. Build your server via a production-classified pipeline that extends 1ES Pipeline Templates. This will automatically run a variety of security scanning tasks and code signing.
7.	Complete the relevant Secure Development Lifecycle (SDL) tasks and compliance review, which should include:
    -  [Threat Model Review](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
    - Verifying the distribution limitations of any licenses used
    - Connecting with your divisional CELA representatives to verify legal coverage and refer to the [GitHub Copilot CELA Guidelines](https://eng.ms/docs/cloud-ai-platform/devdiv/one-engineering-system-1es/1es-jacekcz/ospoost/ai-guidance-for-microsoft-developers/github-copilot-guidelines) for additional compliance points
    - Implement authentication into the server as all newly developed 1P servers will require authentication. Teams should follow SFI best practices and avoid shared secrets and PATS. Refer to the [MCP Server Authentication Reference repo](https://github.com/Azure-Samples/mcp-auth-servers) for examples implementing authentication for the server. This is a repository developed for demo purposes only and is not to be treated as a prescriptive example of full authentication and authorization work for production level resources
    - **Remediate any high and critical vulnerabilities detected from security tasks in your pipeline scan (e.g.: Component Governance, CodeQL, etc.).**

### Publishing Steps
> [!IMPORTANT]
> Local MCP servers require additional packaging steps. Follow steps 1 - 4 for teams publishing out of Azure Pipelines. Please note that this is utilizing a public Artifacts feed Do not share any confidental information through metadata. Ensure server-level authentication implemented for your server prior to publishing.  

1.	Create or re-use your team’s managed identity (MI) or service principal (SP) to perform cross-organization publishing of your MCP server package. For GitHub, see [Quickstart: Use GitHub Actions to push to Azure Artifacts](https://learn.microsoft.com/azure/devops/artifacts/quickstarts/github-actions?view=azure-devops&pivots=managed-identity).
1.	Open a request at aka.ms/MCPServerRequest if you do not have an existing issue, sharing your team's MI/SP GUID and the Azure DevOps organization you're publishing from in the issue. 
1. Set up a service connection to Azure DevOps. This feature is currently in preview, so the 1ES MCP team will work with the ADO team to get your ADO organization enrolled.
1.	After we’ve confirmed your MI/SP now has Feed Contributor permissions, publish your server package to the 1es-mcp-registry Artifacts feed.
1.	Create OneDrive links for all required SDL and compliance artifacts and attach a link to the opened issue in the `ai-for-developers` repo for verification that you completed required compliance and SDL checks
1.	The 1ES team will then surface your MCP server in [aka.ms/MCPRegistry](https://aka.ms/MCPRegistry) and integrated with the 1ES MCP registry used by VS Code and Visual Studio. 
1. (Optional): If interested in 3P consumption, submit a PR to [mcp](https://github.com/microsoft/mcp)
   - Attach a link to the opened issue in the `ai-for-developers` repo for verification that you completed required compliance and SDL checks

## Retiring an MCP Server

If interested in retiring servers developed for 1P consumption, teams should [open an issue in the ai-for-developers repo](https://aka.ms/MCPServerRequest) requesting the entry be removed from listing. If the server has been listed for 3P consumption, raise a PR in the [mcp](https://github.com/microsoft/mcp) repo for removal.

## Additional questions or feedback
If you have feedback or questions that are not covered in this guidance, please create a thread in the [Publishing channel in the MCP @ Microsoft Teams](https://teams.microsoft.com/l/channel/19%3A618ed13e95e743daafc61b4197d6aada%40thread.tacv2/MCP1pPublishing?groupId=f0862597-cf3d-4ec7-beee-1c025c558363&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47)

