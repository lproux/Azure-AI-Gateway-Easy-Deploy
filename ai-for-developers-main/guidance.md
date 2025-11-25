---
layout: page
title: AI Tools for Microsoft Developers
description: "AI Tools for Microsoft Developers"
permalink: /
---
# Microsoft engineers, source code, and AI dev tools

_The scope of this doc is Microsoft engineers and their daily development environment._

Our developer tools business depends on the success of GitHub Copilot. Our engineers build leading-edge AI by dogfooding AI in their daily engineering flow.

We do not block most generative AI at the firewall: we need to be evaluating and deeply understanding the competitive landscape. However, Microsoft **engineers should dogfood our tools before adopting third party tools for use in development.**

Our engineers should use first party tools for development in order to protect Microsoft IP and provide feedback. When a Microsoft engineer uses a competitive offering (e.g. Cursor, ChatGPT), we deprive ourselves of valuable telemetry and [EngThrive](https://aka.ms/engthrive) data. Furthermore, third party tools present a risk of indexing proprietary code, customer code/data, partner code/data, internal business information, and anything that constitutes "Confidential Information" as defined by the [Confidential Information Policy](https://microsoft.sharepoint.com/sites/mspolicy/SitePages/PolicyProcedure.aspx?policyprocedureid=MSPOLICY-804079558-11&CT=1743441799750&OR=OWA-NT-Mail&CID=c1c860fe-922f-35b2-b14c-c59be6211071) (collectively, "Sensitive IP"). _For example, asking ChatGPT "teach me about joining Kusto data" is OK, but "here are specific names of Microsoft tables and real output I need, write a join" is not OK._ In addition, third party tools may output suggestions that violate copyrights and/or open source licenses.

Third-party AI tools should not be used with Microsoft customer data.

Engineers looking to evaluate third party offerings to obtain competitive intelligence (including benchmarking) must review the [Competitive Intelligence Guidance](https://microsoft.sharepoint.com/sites/CELAWeb-BusinessConduct/SitePages/competitive-intelligence.aspx) and, if required, submit a request for [Competitive Intelligence Review](https://microsoft.sharepoint.com/teams/CELACompetitiveIntelligenceReview/SitePages/Submit-your-CI-Request.aspx#fill-out-the-request-form). For product development purposes, engineers may use third party tools as described in this guidance.

For some third party tools, enterprise licenses or negotiated licenses offer training and telemetry guarantees. Teams looking to use third party offerings under enterprise licenses or negotiated licenses should work with frontline CELA and procurement to obtain licenses and approval before use.

There is nuance: while Anthropic Claude's web site is not approved for use with Sensitive IP, Claude _within_ GitHub Copilot with 1ES enterprise access was approved by Microsoft/GitHub CELA and SSPA for Microsoft use. Similarly, third party AI tools like Cline should be run using first party models, like those available on GitHub Copilot Enterprise, or local models when possible.

With any third party AI tools or models, developers should be wary of accepting lengthy code suggestions, as they may match segments of code used to train the models and violate third party copyrights or open source licenses. While there is no bright line regarding how much copying constitutes infringement, suggestions that are 8 lines of code or more pose a high risk. If the suggestion is 8 lines of code or more, the developer should avoid copying the suggestion unless they can locate and review the code's license. Also, developers should have their frontline CELA review the terms of use for any third party AI tool to ensure that it does not contain any restrictions on commercial use, ownership claims to IP, or other terms presenting legal risk. The below table represents the 1ES team's evaluation of certain third party tools. For guidance on legal issues associated with use of these tools, product teams should connect with their frontline CELA.

## Generative AI Developer Desktop Tools

**The table previously here can be found in a summarized form [on the main page](index.md) here on Eng Hub.**

## AI Models & Sensitive IP including Microsoft internal code

Developers should not be using generative AI chat applications and models if it sends Sensitive IP over the wire. Microsoft procurement has **not** broadly approved the use of Claude, Cursor, Gemini, or other products as of April 2025.

A unique exception is that the GitHub Copilot Enterprise product has a model picker with
options to use Claude and Gemini via GitHub Copilot. GitHub Copilot model picker has been
pre-approved for use by Microsoft engineers (see [GitHub Copilot Use Guidelines](https://aka.ms/copilot/guidelines)). 
Please note that Copilot's Gemini models run on Google Cloud Platform and Claude models 
run on Amazon Web Services (Bedrock). Information about how Copilot serves these models can 
be found here: [How Copilot serves AI models - GitHub Docs](https://docs.github.com/en/enterprise-cloud@latest/copilot/reference/ai-models/how-copilot-serves-ai-models).

To use the pre-approved Claude, Gemini, and Open AI models, simply use the 1ES-provided GitHub Copilot Enterprise product. At this time, the GitHub Models product is not available for use at Microsoft.

| Model Provider | General Use | With GitHub Copilot | Enterprise Model SKUs |
| --- | --- | --- | --- |
| Anthropic Claude | Not approved | OK w/ 1ES [Enterprise SKU](https://aka.ms/copilot) | Requires CELA/SSPA review |
| Google Gemini | Not approved | OK w/ 1ES [Enterprise SKU](https://aka.ms/copilot) | Requires CELA/SSPA review |
| OpenAI | Not approved | OK w/ 1ES [Enterprise SKU](https://aka.ms/copilot) | Requires CELA/SSPA review |

Please note that **non-development** use of third party models, such as integration in products, must meet the requirements in the [Checklist for Using Third Party Models](https://docs.opensource.microsoft.com/legal/cela-guidance/checklist-for-using-third-party-models/) and be reviewed by CELA. Submit requests for CELA review using the [Third Party AI Models CELA Review](https://microsoft.sharepoint.com/sites/AIReviews) tool.

## Local models and tools guidance

Consider these [best practices for understanding local models and any risks](https://docs.cline.bot/running-models-locally/read-me-first). It is important that Sensitive IP not be sent to external services that may retain or train on our information. Local models which keep all interactions on a developer's machine are likely a great interim step to unblock creativity. Third party tools like Cline can be used with GitHub Copilot to help maintain the compliance boundary.

Protocols for LLM integration, such as Model Context Protocol (MCP), are emerging in the field. If the protocols are OSS, they should be approached using the established [guidelines for using OSS](https://aka.ms/opensource/using). If the protocols are proprietary, seek frontline CELA review as you would for any third party proprietary software. When possible, use first party implementations of the technology.

Longer-term, it is the vision of Azure AI Foundry and other Microsoft groups to provide a single centralized place for models. Things are evolving quickly.

## Scenario examples

- Think before pasting Sensitive IP, i.e. Windows encryption logic, into a chatbot.
- Do not paste work email into Google Gemini.
- There's a difference between the underlying model and the 3rd-party tool or service using it. Want to use Claude Sonnet 3.7 Thinking as a dev? Use it within GitHub Copilot Enterprise.
- Using ChatGPT to learn about the public .NET source code is fine, that's public open source code.

## Examples of Sensitive IP

| Category | Examples |
|----------|----------|
| **Source Code** | Internal Microsoft codebases, unreleased features, proprietary algorithms, encryption logic |
| **Internal Tables & Infrastructure** | Names of internal Kusto tables, telemetry pipelines, backend service configurations |
| **Business Information** | Product roadmaps, financial forecasts, internal strategy documents |
| **Emails & Communications** | Internal discussions, confidential project updates, legal or compliance correspondence |
| **Proprietary Models & Prompts** | Prompts or outputs involving internal AI models, Copilot telemetry, or model tuning data |

## Approval requirements

- Third party AI tools requiring purchase must be reviewed by Microsoft Procurement. Procurement prohibits the use of corporate credit cards for SaaS purchases including AI products.
- All use of third party AI tools, APIs, or solutions requires review from frontline CELA, Microsoft Procurement (i.e. SSPA), and Microsoft Digital. Procurement and Microsoft Digital
  review can be initiated using the [Software & Cloud Services Buying Process](https://microsoft.sharepoint.com/teams/MyProcureWeb/SitePages/SoftwareandCloudServices.aspx) outlined
  in the steps [here](https://microsoft.sharepoint.com/teams/MyProcureWeb/SitePages/SoftwareandCloudServices.aspx#purchase-third-party-software-or-cloud-services-not-available-in-the-software-catalog).
  (Note: The Software & Cloud Services Buying Process is required to use any third party solutions, regardless if purchased or free).

## Related resources

- DSR / MSProtect: Using ChatGPT safely and securely [aka.ms/3pgenai](https://aka.ms/3pgenai)
- DSR / MSProtect: Large Language Models overview
- CELA: GitHub Copilot guidelines @ [aka.ms/copilot/guidelines](https://aka.ms/copilot/guidelines)
- CELA: Open Data checklist
- Internal GitHub Copilot adoption dashboard [aka.ms/copilot/slt](https://aka.ms/copilot/slt) reflects use by engineers via 1ES Enterprise SKU. More info at [aka.ms/copilot](https://aka.ms/copilot). Check your own use data at: [aka.ms/copilot/data](https://aka.ms/copilot/data)

> [!tip] This guidance will evolve in FY26. The [internal working document](https://aka.ms/1es/ai-tools-guidance-doc) has historical comments within.
> This EngHub page reflects the content as of 2025-06-17.
