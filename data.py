import csv

examples = []

with open("examples.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        if row['text'] == row['correction']:
            row['correction'] = "No corrections required."
        examples.append(row)


# [
#     {
#         "text": "## Hllo World!",
#         "correction": "## Hello World!",
#     },
#     {
#         "text": "I enjoy using [mardown for documenttion](https://example.com).",
#         "correction": "I enjoy using [markdown for documentation](https://example.com).",
#     },
#     {
#         "text": "* Bullet poitns are usefull",
#         "correction": "* Bullet points are useful",
#     },
#     {
#         "text": "**This is bold text with a tyypo**",
#         "correction": "**This is bold text with a typo**",
#     },
#     {
#         "text": "IBM Catalog Solutions which **requires pre-requisite Schematics Workspace ID**",
#         "correction": "IBM Catalog Solutions **requiring pre-requisite Schematics Workspace ID**",
#     },
#     {
#         "text": "1. [Markdown](https://example.com) Frist item in a list",
#         "correction": "1. [Markdown](https://example.com) First item in a list",
#     },
#     {
#         "text": "![Alt txt](image.jpg)",
#         "correction": "![Alt text](image.jpg)",
#     },
#     {
#         "text": "> Blockqoute with mispellings",
#         "correction": "> Blockquote with misspellings",
#     },
#     {
#         "text": "Use `inline code` to highlight code snippits",
#         "correction": "Use `inline code` to highlight code snippets.",
#     },
#     {
#         "text": "# Header 1 with a mistake",
#         "correction": "# Header 1 with a Mistake",
#     },
#     {
#         "text": "### Thid level header is usefull",
#         "correction": "### Third Level Header is Useful",
#     },
#     {
#         "text": "#### The smallet header",
#         "correction": "#### The Smallest Header",
#     },
#     {
#         "text": "Multi-line text with issues:\n- This is the first line,\n- and this is the secon one.",
#         "correction": "Multi-line text with issues:\n- This is the first line,\n- And this is the second one.",
#     },
#     {
#         "text": "## Headers are important for strcuture",
#         "correction": "## Headers are Important for Structure",
#     },
#     {
#         "text": "My favorite thing about Markdown is it's simplicity and ease of use.",
#         "correction": "What I appreciate most about Markdown is its simplicity and user-friendliness.",
#     },
#     # {
#     #     "text": "Tables are also useful\n| Header 1 | Header 2 |\n| -------- | -------- |\n| Row 1 | Row 2 |",
#     #     "correction": "Tables are also useful\n| Header 1 | Header 2 |\n| -------- | -------- |\n| Row 1    | Row 2    |",
#     # },
#     {
#         "text": "![Image without alt text](image.jpg)",
#         "correction": "![Image without alt text](image.jpg)",
#     },
#     # {
#     #     "text": "```python\nprnt('Hello World!')\n```",
#     #     "correction": "```python\nprint('Hello World!')\n```",
#     # },
#     {
#         "text": "Reference-style links are also valid: [Markdown][1]\n\n[1]: https://example.com",
#         "correction": "Reference-style links are also valid: [Markdown][1]\n\n[1]: https://example.com",
#     },
#     {
#         "text": "IBM Cloud Satellite helps you deploy and run applications consistently across all on-premises, edge computing, and public cloud environments from any cloud vendor. It standardizes a core set of Kubernetes, data, AI, and security services to be centrally managed as a service by IBM Cloud, with full visibility across all environments through a single pane of glass. The result is greater developer productivity and development velocity.",
#         "correction": "IBM Cloud Satellite enables consistent deployment and operation of applications across all on-premises, edge computing, and public cloud environments from various cloud providers. It harmonizes a fundamental set of Kubernetes, data, AI, and security services to be centrally administered as a service by IBM Cloud, offering comprehensive oversight across all environments via a unified interface. This leads to enhanced developer productivity and accelerated development pace.",
#     },
#     {
#         "text": 'This module creates default coarse-grained CBR rules in a given account following a "secure by default" approach - that is: deny all flows by default, except known documented communication in the [Financial Services Cloud Reference Architecture](https://cloud.ibm.com/docs/framework-financial-services?topic=framework-financial-services-vpc-architecture-about):',
#         "correction": 'This module generates default coarse-grained CBR rules in a given account, following a "secure by default" approach - that is, denying all flows by default, except for known documented communication in the [Financial Services Cloud Reference Architecture](https://cloud.ibm.com/docs/framework-financial-services?topic=framework-financial-services-vpc-architecture-about):',
#     },
#     {
#         "text": "# IBM module",
#         "correction": "# IBM Module",
#     },
#     {
#         "text": "Example generating a markdown link: https://cloud.ibm.com/docs/satellite?topic=satellite-getting-started. This is an existing markdown link [About DNS sharing for VPE gateways](https://cloud.ibm.com/docs/vpc?topic=vpc-hub-spoke-model).",
#         "correction": "Example generating a markdown link: [IBM Cloud Satellite Getting Started](https://cloud.ibm.com/docs/satellite?topic=satellite-getting-started). This is an existing markdown link [About DNS sharing for VPE gateways](https://cloud.ibm.com/docs/vpc?topic=vpc-hub-spoke-model).",
#     },
#     {
#         "text": "Creates and configures **1 HANA instance, 0 to N NetWeaver instances and 1 Optional ShareFS** with **RHEL or SLES OS** distribution.",
#         "correction": "Creates and configures **one HANA instance, zero to several NetWeaver instances and one optional ShareFS** with **RHEL or SLES OS** distribution.",
#     },
#     {
#         "text": "The [usage example](../../examples/fscloud/) demonstrates how to set the enforcement mode to 'enabled' for the key protect (\"kms\") service.",
#         "correction": "The [usage example](../../examples/fscloud/) demonstrates how to set the enforcement mode to 'enabled' for the Key Protect (\"kms\") service.",
#     },
#     {
#         "text": """1.  Log in to [IBM Cloud](https://cloud.ibm.com) with the IBMid you used to set up the account. This IBMid user is the account owner and has full IAM access.
# 1.  [Complete the company profile](https://cloud.ibm.com/docs/account?topic=account-contact-info) and contact information for the account. This profile is required to stay in compliance with IBM Cloud Financial Service profile.
# 1.  [Enable the Financial Services Validated option](https://cloud.ibm.com/docs/account?topic=account-enabling-fs-validated) for your account.
# 1.  Enable virtual routing and forwarding (VRF) and service endpoints by creating a support case. Follow the instructions in enabling VRF and service endpoints](https://cloud.ibm.com/docs/account?topic=account-vrf-service-endpoint&interface=ui#vrf).
# """,
#         "correction": """1.  Log in to [IBM Cloud](https://cloud.ibm.com) with the IBMid used to set up the account. This IBMid user is the account owner and has full IAM access.
# 1.  [Complete the company profile](https://cloud.ibm.com/docs/account?topic=account-contact-info) and contact information for the account. This profile is required to stay in compliance with the IBM Cloud Financial Service profile.
# 1.  [Enable the Financial Services Validated option](https://cloud.ibm.com/docs/account?topic=account-enabling-fs-validated) for your account.
# 1.  Follow the instructions in enabling VRF and service endpoints at [IBM Cloud Account Documentation](https://cloud.ibm.com/docs/account?topic=account-vrf-service-endpoint&interface=ui#vrf).
# """,
#     },
#     {
#         "text": "1.  [Set up access groups](https://cloud.ibm.com/docs/account?topic=account-account-getting-started#account-gs-accessgroups).",
#         "correction": "1.  [Set up access groups](https://cloud.ibm.com/docs/account?topic=account-account-getting-started#account-gs-accessgroups).",
#     },
#     {
#         "text": "    Please live the spaces and tabs as in te original.",
#         "correction": "    Please leave the spaces and tabs as in the original.",
#     },
#     {
#         "text": '![Architecture diagram of the OpenShift Container Platform on VPC deployable architecture](roks.drawio.svg "Architecture diagram of Red Hat OpenShift Container Platform on VPC landing zone deployable architecture"){{: caption="Figure 1. Single region architecture diagram for Red Hat OpenShift Container Platform on VPC on IBM Cloud" caption-side="bottom"}}{{: external download="roks.drawio.svg"}}',
#         "correction": '![Architecture Diagram of OpenShift Container Platform on VPC Deployable Architecture](roks.drawio.svg "Architecture Diagram of Red Hat OpenShift Container Platform on VPC Landing Zone Deployable Architecture"){{: caption="Figure 1. Single Region Architecture Diagram for Red Hat OpenShift Container Platform on VPC on IBM Cloud" caption-side="bottom"}}{{: external download="roks.drawio.svg"}}',
#     },
#     {
#         "text": """# Use if the reference architecture has deployable code.
# # Value is the URL to land the user in the IBM Cloud catalog details page
# # for the deployable architecture.
# # See https://test.cloud.ibm.com/docs/get-coding?topic=get-coding-deploy-button
# deployment-url: https://cloud.ibm.com/catalog/architecture/deploy-arch-ibm-slz-ocp-95fccffc-ae3b-42df-b6d9-80be5914d852-global""",
#         "correction": """# Use if the reference architecture has deployable code.
# # Value is the URL to land the user in the IBM Cloud catalog details page
# # for the deployable architecture.
# # See https://test.cloud.ibm.com/docs/get-coding?topic=get-coding-deploy-button
# deployment-url: https://cloud.ibm.com/catalog/architecture/deploy-arch-ibm-slz-ocp-95fccffc-ae3b-42df-b6d9-80be5914d852-global""",
#     },
#     {
#         "text": "To set up your local development environment, see [Local development setup](https://terraform-ibm-modules.github.io/documentation/#/local-dev-setup) in the project documentation.",
#         "correction": "To set up your local development environment, see [local development setup](https://terraform-ibm-modules.github.io/documentation/#/local-dev-setup) in the project documentation.",
#     },
#     {
#         "text": "- Data retention, [lifecycle](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-archive) and archiving options",
#         "correction": "- Data retention, [lifecycle](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-archive), and archiving options.",
#     },
#     {
#         "text": """- IBM Cloud VPC Infrastructure Services (IS) -> Cloud Object Storage (COS)
# - Virtual Private Cloud workload (eg: Kubernetes worker nodes) -> IBM Cloud Container Registry""",
#         "correction": """- IBM Cloud VPC Infrastructure Services (IS) -> Cloud Object Storage (COS)
# - Virtual Private Cloud workload (e.g., Kubernetes worker nodes) -> IBM Cloud Container Registry"""
#     },
#     {
#         "text": """See in particular the [fscloud module](./modules/fscloud/) that enables creating an opiniated account-level coarse-grained set of CBR rules and zones aligned with the "secure by default" principles.""",
#         "correction": """Please refer to the [fscloud module](./modules/fscloud/) for creating an opinionated account-level coarse-grained set of CBR rules and zones that align with the "secure by default" principles."""
#     },
#     {
#         "text": """## Overview
# * [terraform-ibm-cbr](#terraform-ibm-cbr)
# * [Submodules](./modules)
#     * [cbr-rule-module](./modules/cbr-rule-module)""",
#         "correction": """## Overview
# * [terraform-ibm-cbr](#terraform-ibm-cbr)
# * [Submodules](./modules)
#     * [cbr-rule-module](./modules/cbr-rule-module)"""
#     },
#     {
#         "text": """use-case: ITServiceManagement
# industry: Technology""",
#         "correction": """use-case: ITServiceManagement
# industry: Technology"""
#     }
# ]
