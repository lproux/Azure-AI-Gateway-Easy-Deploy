---
title: GitHub Copilot Guidance
layout: page
---

# Use of GitHub Copilot at Microsoft

<!--
NOTE: this page was relocated from the "open source docs" repo to the 1ES AI eng hub repo to consolidate and simplify, since
GitHub Copilot is a general developer tool and not open source-specific. The previous commit history can be reviewed at
https://github.com/opensource-microsoft/docs/commits/main/docs/legal/cela-guidance/copilot.md
-->

**GitHub Copilot Enterprise is pre-approved for use** by all Microsoft
employees, interns and vendors for Microsoft work using
[1ES-provided Copilot Enterprise](https://aka.ms/copilot), unless you are
working on a
[tented project](https://microsoft.sharepoint.com/:w:/r/sites/mspolicy/_layouts/15/doc2.aspx?sourcedoc=%7B60DD8C2B-B195-448A-B7D5-055621D95FDB%7D&file=Corporate%20Tenting%20Policy.docx&action=default&mobileredirect=true),
a government project subject to government data handling controls, or you have
been informed that your project data may not leave its country of origin. Once
added to your personal GitHub account, GitHub Copilot Enterprise can also be
used for home and hobby projects. GitHub Copilot Free should not be used for
Microsoft work. [Review FAQ topics](github-copilot-faq.md)

<!-- prettier-ignore-start -->
<!-- NOTE: the source of truth for this section is at:
     https://github.com/1ES-microsoft/opensource-management-portal/blob/trunk/microsoft/copilot/agreements/fy25_q2_html.ts
     -->
<h2 class="body-heading">GitHub Copilot Use Guidelines</h2> 
<p class="body-text">
  <strong>You are responsible for the code you write with GitHub Copilot.</strong> 
  When using Copilot, be sure to follow existing team practices for source
  code - the coding suggestions you accept should abide by the same policies
  that apply to code you write without GitHub Copilot, for example,
  <a href="https://aka.ms/sdl" target="_new">Security Development Lifecycle (SDL)</a>
  requirements for your organization.
</p>
<p class="body-text">
  <strong>Repo exclusion feature. </strong>
  Teams may use the Windows GitHub Copilot v-team's repo exclusion feature where
  needed to limit the code that GitHub Copilot has access to. These configurations can be
  used, for example, to restrict Copilot from using a folder containing third-party
  code to generate suggestions. You can learn more about the feature at 
  <a href="https://aka.ms/copilot/repository-exclusion">aka.ms/copilot/repository-exclusion</a>. 
  <strong>If you are a dev manager of a team that handles 3rd-party code subject to use restrictions</strong> 
  <a target="_new" href="https://aka.ms/copilot/guidelines/tented">see additional guidance</a>.
</p>
<p class="body-text">
  <strong>Customer data. </strong>
  GitHub Copilot should not be used on customer data.
</p>
<p class="body-text">
  <strong>Source code and data collection notice. </strong> 
  Code snippets and user engagement data may be used by Microsoft and GitHub for
  abuse detection and model improvement. See the
  <a href="https://github.com/features/copilot/" target="_new">feature page</a> 
  for more information on data collection. This collection will also apply to personal
  GitHub accounts linked to the Microsoft Copilot organization.
</p>
<p class="body-text">
  <strong>Model Picker. </strong>
  For more information about various models, review the <a href="https://aka.ms/1es/ai-tools-guidance-full" target="_new">Microsoft internal AI Tools guidance page</a>.
</p>
<p class="body-text">
  <strong>Mandatory Copilot code reference review instructions. </strong><br />
  <strong>If the suggestion is <= 8 lines of code:</strong> No review is needed<br />
  <strong>If the suggestion is > 8 lines of code:</strong> In the Output Window, make sure GitHub Copilot Log is selected 
  in the pulldown on the right hand side of the window in order to see any license alerts for similar code. Determine 
  whether or not you can accept the suggestion by reviewing the below.<br />
  <strong>DO NOT to accept a suggestion: If the only or OLDEST license(s) on code suggestion</strong> is 
  <a href="https://docs.opensource.microsoft.com/legal/resources/oss-licenses-by-type/#weak-copyleft-licenses" target="_new">Weak Copyleft</a>, 
  <a href="https://docs.opensource.microsoft.com/legal/resources/oss-licenses-by-type/#strong-copyleft-licenses" target="_new">Copyleft</a>, or 
  <a href="https://docs.opensource.microsoft.com/legal/resources/oss-licenses-by-type/#network-copyleft-licenses" target="_new">Network Copyleft</a>  
  (e.g. GPL, AGPL, LGPL, EPL), do NOT accept the suggestion. Microsoft needs the ability to use code in any way 
  moving forward, including in ways where we must keep the source code closed upon distribution.
  <br />
  <strong>YOU MAY accept a suggestion:</strong> If the code suggestion's reported license is one or more 
  <a href="https://docs.opensource.microsoft.com/legal/resources/oss-licenses-by-type/#permissive-oss-licenses" target="_new">Permissive</a> licenses, then you are responsible for including 
  copyright and license attribution for the first code suggestion [License; Link to Repository] in the 
  <a href="https://docs.opensource.microsoft.com/using/guidance-for-open-source-usage/notice-faq/" target="_new">NOTICE file</a> of 
  your product, if 
  <a href="https://docs.opensource.microsoft.com/legal/resources/GLOSSARY/#distribution" target="_new">distributed</a>.
  <br />
  For questions, contact the <a href="mailto:OSSOM@service.microsoft.com">OSS Standards Open ML (OSSOM) legal team</a>.
</p>
<p class="body-text">
  See <a target="_new" href="https://aka.ms/copilot/guidelines/third-party">these additional guidelines and approvals required</a> for use of GitHub Copilot
  for tented projects and government projects subject to government data handling controls.
</p>
<p class="body-text">
  <strong>Flag potential problems. </strong>
  Contact <a href="mailto:copilot-safety@github.com">copilot-safety@github.com</a> if
  you identify privacy, security, offensive content, or other issues in Copilot
  suggestions.
</p>

<details>
  <summary>Tented and Government Projects Subject to Government Data Handling Controls</summary>
  <p>
    Please review the guidance below and seek pre-approval of the project manager
    to use GitHub Copilot on tented or government projects subject to government data handling controls (including
    projects with classified data, unclassified data, or trade restricted data).
  </p>  
  <p>
    As code snippets and user engagement data from 1ES-provided 
    Copilot Enterprise may be used by limited Microsoft/GitHub employees for 
    abuse detection and model improvement, such employees may learn information 
    about your tented/sensitive government project if disclosed in a prompt or
    suggestion. Additionally, GitHub Copilot may load balance processing of 
    Code Snippet Data and User Engagement Data across global infrastructure such 
    that data is processed (but not stored) outside of the country in which a 
    request originates (e.g., GitHub Copilot may process data from a
    United States repo outside the United States).
  </p>
  <p>
    <strong>Project Managers, </strong> before approval of a project, please 
    carefully review the 
    <a target="_new" href="https://resources.github.com/copilot-trust-center/">data collection and use information</a>
    and determine what repositories, if any, GitHub Copilot 
    should be restricted from accessing using the 
    <a href="aka.ms/copilot/repository-exclusion" target="_new">repo exclusion feature</a> to avoid 
    inadvertent disclosure of information. If you have any further questions, 
    please reach out to <a href="https://findcontact.microsoft.com/" target="_new">your CELA contact</a>.
  </p>
</details>

<details><summary>Engineering teams using 3rd-party code subject to use restrictions</summary>
  <p>
    In rare circumstances, Microsoft's contracts with 3rd parties may place 
    limitations on the use of such 3rd party code for generation of 
    GitHub Copilot outputs. This issue can be addressed by using the repo 
    exclusion feature to block Copilot’s access to certain 3rd party files. 
    Please carefully review the data collection and use information available 
    on the feature page and determine what repositories, if any, should be 
    restricted. If you have any further questions, please reach out 
    to <a href="mailto:cpquestions@microsoft.com">cpquestions@microsoft.com</a>.

  </p>
  <p>
    If you are on the Windows Engineering team, there is no need to take 
    further action to exclude files as this has already been addressed 
    by Windows Engineering 
    (<a href="https://eng.ms/docs/cloud-ai-platform/azure-edge-platform-aep/aep-engineering-systems/productivity-and-experiences/developer-productivity/wave-for-windows-azure/copilot/overview" target="_new">see here</a>).
  </p>
</details>
<!-- prettier-ignore-end -->

## How to get access

<!-- prettier-ignore-start -->
> [!tip]
> **IMPORTANT** don't sign up for Copilot using the GitHub website: all
> Microsoft full-time employees (FTEs and interns) already have access using their
> GitHub Enterprise account. Visit [aka.ms/copilot/explore](https://aka.ms/copilot/explore)
> to automatically sign in as your GitHub Enterprise account and learn more. To add
> Copilot to your personal GitHub account, visit [aka.ms/copilot](https://aka.ms/copilot).
> _You can use the Microsoft-provided Copilot access for personal and home use, too._
{: .protip .mb-6}
<!-- prettier-ignore-end -->

Access is available two ways, either with your individual GitHub account, and/or
your Enterprise Managed Users (EMU) account. The quickest way to get access
today is to use the EMU account.

If you have any issues, please
[review the videos on the Copilot at Microsoft FAQ](https://aka.ms/gim/copilot).

### Enterprise Managed User (EMU) access

Microsoft employees have a **GitHub Enterprise Cloud with Enterprise Managed
Users (EMU) account** that is for internal engineering use. The GitHub username
is automatic, and is `YOURALIAS_microsoft`. For example, ScottGu's account is
`scottgu_microsoft`.

If you are an FTE or intern, as of February 2024, you already have access. To
authenticate with your account that has access and learn more:

1. Navigate to [https://aka.ms/copilot/explore](https://aka.ms/copilot/explore)
   in your default web browser.
2. You can try Copilot in a Codespace, or, install the extensions and
   authenticate.

_There is a [Copilot on EMU troubleshooting guide](https://aka.ms/gim/copilot)
available if needed plus
[lots of cool internal GitHub Copilot videos](https://aka.ms/copilot/videos)._

### Access with your linked GitHub.com account

Follow these steps to enable your individual (personal) GitHub Account to use
GitHub Copilot. An individual account is a GitHub username that _you_ create,
manage the password for, and link for open source use at Microsoft. It is
separate from your corporate GitHub Enterprise (EMU) account. Your individual
account remains yours if you leave Microsoft (though you free Copilot access
ends if you leave).

1. Have a GitHub account or create one at
   [https://github.com](https://github.com). GitHub Accounts used for Microsoft
   work must have two-factor authentication turned on. You can choose to use
   your individual account or create one distinctly for work use. See also
   [GitHub account guidance](https://docs.opensource.microsoft.com/github/opensource/accounts/).
2. Link your GitHub account for company use at
   [https://aka.ms/opensource/portal](https://aka.ms/opensource/portal). This
   associates your GitHub account with your company account so that you can
   publish open source and access private repositories at Microsoft. You can
   also choose to join other Microsoft organizations on GitHub and opt-in for
   Copilot access.
3. Navigate to [https://aka.ms/copilot](https://aka.ms/copilot).
   - Agree to the guidelines to receive an invitation to the `MicrosoftCopilot`
     organization on GitHub that grants access to Copilot. **You'll need to
     accept the invite to the MicrosoftCopilot org to use Copilot**.
4. Follow the
   [GitHub Copilot Getting Started Docs](https://docs.github.com/en/copilot) to
   install the appropriate extensions for the product and authenticate with your
   GitHub account.

## Resources

### Security and other compliance reviews

DSR completed a preliminary review of the Copilot developer extension in early
2023 and approved its use for developer productivity in association with these
specific opt-in guidelines for employees and the understanding that employees
are responsible for the code that they write.

### Copilot features access

Microsoft is dogfooding Copilot and often will have early access to features
such as Copilot Enterprise, including chat experiences right on the github.com
web site, and more.

Please see
[the breakdown of Copilot features and availability at aka.ms/copilot](https://aka.ms/copilot/features).

### Copilot onboarding data and dashboards

Across Microsoft, onboarding data is used to track adoption of this exciting
productivity tool. The primary dashboard can be found at
[aka.ms/copilot/slt](https://aka.ms/copilot/slt).

#### Data narrative

The 1ES-enabled usage of Copilot is split across several GitHub Enterprises that
Microsoft engineers use. We get accurate data as a Copilot product feature that
tells us the last time a given user connected to Copilot and from what editor.
These two pieces of information drive the bulk of the reporting as it can tell
us if someone has ever used Copilot, or has not used it in a while etc.

We do not have access to any data at the individual level that is not contained
in the product-reported dataset. We are working with GitHub to help define their
roadmap for providing data to all Copilot Enterprise customers.

Starting in 2024, GitHub began providing more high-level utilization info, such
as the number of suggestions shown and accepted by language and editor, but only
at aggregate levels. In 2025, this space will evolve further.

### Information about using generative AI at Microsoft

For more information on the use of third-party tools with Microsoft data in
general, please visit [aka.ms/3PGenAI](https://aka.ms/3PGenAI).

### Contacts

For general Copilot product feedback and support:

- GitHub's
  [Copilot public feedback forum](https://github.com/community/community/discussions/categories/copilot)
- [GitHub Support](https://support.github.com/contact)

For technical Copilot onboarding and access issues:

- [email](mailto:cpquestions@microsoft.com) or
  [GitHub discussions (EMU)](https://aka.ms/github/copilot/discussions)

Onboarding, access and rollout programs:

- Dashboard is managed by
  [Mark Phippard, 1ES GitHub inside Microsoft PM](mailto:MARKPHIPPARD@microsoft.com).
- Copilot onboarding portal is managed by
  [Jeff Wilcox, DevDiv TPM](mailto:JWILCOX@microsoft.com).
- GitHub Copilot at Microsoft questions should go to
  [CPQuestions@microsoft.com](mailto:cpquestions@microsoft.com).
