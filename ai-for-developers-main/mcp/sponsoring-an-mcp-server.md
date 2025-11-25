# Sponsoring a third-party MCP server 

----

A third-party (3P) MCP server is one that is originally developed by someone outside of Microsoft. 3P MCP servers must be **sponsored** before internal use. Sponsoring means that there is a team within Microsoft that ensures the 3P MCP server is secure by rebuilding it from source, running it through the Secure Development Lifecycle (SDL), creating a central point of distribution, and ensuring that the code keeps up with upstream OSS changes.

**Do not directly consume a 3P MCP server, even if it is only running locally.** 

## Path to 3P MCP usage

To start using a 3P MCP server: 
1. Fill out this GitHub issue at [https://aka.ms/MCPSurvey3P](https://aka.ms/MCPSurvey3P) and highlight a 3P MCP server you and your team want to sponsor.
1. The 1MCP team will review and approve your server.
1. Rebuild the 3P MCP server, following the [“Using open source at Microsoft” guidelines](https://docs.opensource.microsoft.com/using/), similar to any other open-source software. Review the ["Rebuilding projects" guidance](https://docs.opensource.microsoft.com/using/guidance-for-open-source-usage/rebuilding/) as well. You do not need to maintain a hard fork of the project, but you do need to use a 1ES Pipeline Template-extended pipeline to build and scan the project. 
1. Complete the checklist under [Rebuilding the MCP server](#rebuilding-the-mcp-server).
1. Your 3P MCP server is now ready for use internally.

See [MCP Servers at Microsoft](index.md) for general guidance on MCP servers within the company.

## Rebuilding the MCP server

Note: Before rebuilding any 3P MCP server, please confirm that the server's license does not present legal risks - either by using Component Governance or by sending the license to your frontline CELA for review.

1. Follow steps 5 and 6 on our [Publishing an MCP server guidance](https://eng.ms/docs/cloud-ai-platform/devdiv/one-engineering-system-1es/1es-jacekcz/ospoost/ai-guidance-for-microsoft-developers/mcp/publishing-an-mcp-server#publishing-an-mcp-server) to ensure that your repo and pipeline creation are secure and compliant with SDL and compliance requirements.
1. Once the pipeline completes successfully with no detected supply chain vulnerabilities and no failed SDL tasks, you can clone the repository into your local environment and run the MCP server safely. 
1. At this point, distribution and installation of MCP servers is not standardized. For consistency, try to use the same distribution mechanism as the OSS repo, but hosted on a Microsoft asset. For internal only local servers, the recommended path is to upload the package as an Azure Artifacts package. See [Figma-Context-MCP](https://dev.azure.com/msazure/One/_git/Figma-Context-MCP) server for reference.
1. Check **Compliance** > **Component Governance** and confirm you have no open alerts. Additionally, it is recommended to run the server as an HTTP Server-Sent Events (SSE) type to monitor all logs and control the process.
1. Update your issue from the [1es-for-developers](https://github.com/1es/ai-for-developers/issues) repository to let us know that your server is now available for consumption.

Happy coding!
