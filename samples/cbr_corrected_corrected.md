## Pre-wired CBR configuration for FS Cloud

This module generates default coarse-grained CBR rules in a given account, following a "secure by default" approach - that is, denying all flows by default, except for known documented communication in the [Financial Services Cloud Reference Architecture](https://cloud.ibm.com/docs/framework-financial-services?topic=framework-financial-services-vpc-architecture-about):
- Cloud Object Storage (COS) -> Key Management Service (KMS)
- Block Storage -> Key Management Service (KMS)
- IBM Cloud Kubernetes Service (IKS) -> Key Management Service (KMS)
- All IBM Cloud Databases (ICD) services -> Key Management Service (KMS)
- Activity Tracker route -> Cloud Object Storage (COS)
- Virtual Private Clouds (VPCs) where clusters are deployed -> Cloud Object Storage (COS)
- IBM Cloud VPC Infrastructure Services (IS) -> Cloud Object Storage (COS)
- Virtual Private Cloud workload (e.g., Kubernetes worker nodes) -> IBM Cloud Container Registry
- IBM Cloud Databases (ICD) -> Hyper Protect Crypto Services (HPCS)
- IBM Cloud Kubernetes Service (IKS) -> IS (VPC Infrastructure Services)


**Note on KMS**: The module supports setting up rules for Key Protect and Hyper Protect Crypto Services. By default, the module sets rules for Hyper Protect Crypto Services, but this can be modified to use Key Protect, Hyper Protect, or both Key Protect and Hyper Protect Crypto Services using the input variable `kms_service_targeted_by_prewired_rules`.

Note on containers-kubernetes: the module supports the pseudo-service names `containers-kubernetes-management` and `containers-kubernetes-cluster` to distinguish between the cluster and management APIs (see [details](https://cloud.ibm.com/docs/containers?topic=containers-cbr&interface=ui#protect-api-types-cbr) ). The module creates separate CBR rules for the two types of APIs by default to align with common real-world scenarios. `containers-kubernetes` can be used to create a CBR targeting both the cluster and management APIs.

This module is designed to allow the consumer to add additional custom rules to open up additional flows necessarity for their usage. See the `custom_rule_contexts_by_service` input variable, and an [usage example](../../examples/fscloud/) demonstrating how to open up more flows.

The module also pre-creates CBR zones for each service in the account as a best practice. CBR rules associated with these CBR zones can be set by using the `custom_rule_contexts_by_service` variable.

Important: To avoid unexpected breakage in the account against which this module is executed, the CBR rule enforcement mode is set to 'report' (or 'disabled' for services not supporting 'report' mode) by default. It is recommended to test this module first with these default settings and then use the `target_service_details` variable to set the enforcement mode to "enabled" gradually by service. The [usage example](../../examples/fscloud/) demonstrates how to set the enforcement mode to 'enabled' for the Key Protect ("kms") service.

## Note
The services 'compliance', 'directlink', 'iam-groups', 'containers-kubernetes', 'user-management' does not support restriction per location.

### Usage

```hcl
module "cbr_fscloud" {
  source           = "terraform-ibm-modules/cbr/ibm//modules/fscloud"
  version          = "X.X.X" # Replace "X.X.X" with a release version to lock into a specific release
  prefix                           = "fs-cbr"
  zone_vpc_crn_list                = ["crn:v1:bluemix:public:is:us-south:a/abac0df06b644a9cabc6e44f55b3880e::vpc:r006-069c6449-03a9-49f1-9070-4d23fc79285e"]

  # True or False to set prewired rule
  allow_cos_to_kms                 = true
  allow_block_storage_to_kms       = true
  allow_roks_to_kms                = true
  allow_icd_to_kms                 = true
  allow_vpcs_to_container_registry = true
  allow_vpcs_to_cos                = true
  allow_at_to_cos                  = true
  allow_iks_to_is                  = true

  # Will skip the zone creation for service ref. present in the list
  skip_specific_services_for_zone_creation = ["user-management", "iam-groups"]

  target_service_details = {
                            "kms" = {
                              "enforcement_mode" = "enabled"
                           }}

  custom_rule_contexts_by_service = {
                                    "schematics" = [{
                                      endpointType = "public"
                                      zone_ids     = "93a51a1debe2674193217209601dde6f" # pragma: allowlist secret
                                    }]
                                  }
}
```

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
### Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.3.0, <1.6.0 |
| <a name="requirement_ibm"></a> [ibm](#requirement\_ibm) | >=1.56.1 |

### Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_cbr_rule"></a> [cbr\_rule](#module\_cbr\_rule) | ../../modules/cbr-rule-module | n/a |
| <a name="module_cbr_zone"></a> [cbr\_zone](#module\_cbr\_zone) | ../../modules/cbr-zone-module | n/a |
| <a name="module_cbr_zone_deny"></a> [cbr\_zone\_deny](#module\_cbr\_zone\_deny) | ../../modules/cbr-zone-module | n/a |
| <a name="module_cbr_zone_vpcs"></a> [cbr\_zone\_vpcs](#module\_cbr\_zone\_vpcs) | ../../modules/cbr-zone-module | n/a |

### Resources

| Name | Type |
|------|------|
| [ibm_iam_account_settings.iam_account_settings](https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs/data-sources/iam_account_settings) | data source |

### Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_allow_at_to_cos"></a> [allow\_at\_to\_cos](#input\_allow\_at\_to\_cos) | Set rule for Activity Tracker to COS, default is true | `bool` | `true` | no |
| <a name="input_allow_block_storage_to_kms"></a> [allow\_block\_storage\_to\_kms](#input\_allow\_block\_storage\_to\_kms) | Set rule for block storage to KMS, default is true | `bool` | `true` | no |
| <a name="input_allow_cos_to_kms"></a> [allow\_cos\_to\_kms](#input\_allow\_cos\_to\_kms) | Set rule for COS to KMS, default is true | `bool` | `true` | no |
| <a name="input_allow_icd_to_kms"></a> [allow\_icd\_to\_kms](#input\_allow\_icd\_to\_kms) | Set rule for ICD to KMS, deafult is true | `bool` | `true` | no |
| <a name="input_allow_iks_to_is"></a> [allow\_iks\_to\_is](#input\_allow\_iks\_to\_is) | Set rule for IKS to IS (VPC Infrastructure Services), default is true | `bool` | `true` | no |
| <a name="input_allow_is_to_cos"></a> [allow\_is\_to\_cos](#input\_allow\_is\_to\_cos) | Set rule for IS (VPC Infrastructure Services) to COS, default is true | `bool` | `true` | no |
| <a name="input_allow_roks_to_kms"></a> [allow\_roks\_to\_kms](#input\_allow\_roks\_to\_kms) | Set rule for ROKS to KMS, default is true | `bool` | `true` | no |
| <a name="input_allow_vpcs_to_container_registry"></a> [allow\_vpcs\_to\_container\_registry](#input\_allow\_vpcs\_to\_container\_registry) | Set rule for VPCs to container registry, default is true | `bool` | `true` | no |
| <a name="input_allow_vpcs_to_cos"></a> [allow\_vpcs\_to\_cos](#input\_allow\_vpcs\_to\_cos) | Set rule for VPCs to COS, default is true | `bool` | `true` | no |
| <a name="input_custom_rule_contexts_by_service"></a> [custom\_rule\_contexts\_by\_service](#input\_custom\_rule\_contexts\_by\_service) | Any additional context to add to the CBR rules created by this module. The context are added to the CBR rule targetting the service passed as a key. The module looks up the zone id when service\_ref\_names or add\_managed\_vpc\_zone are passed in. | <pre>map(list(object(<br>    {<br>      endpointType = string # "private, public or direct"<br><br>      # Service-name (module lookup for existing network zone) and/or CBR zone id<br>      service_ref_names    = optional(list(string), [])<br>      add_managed_vpc_zone = optional(bool, false)<br>      zone_ids             = optional(list(string), [])<br>  })))</pre> | `{}` | no |
| <a name="input_existing_cbr_zone_vpcs"></a> [existing\_cbr\_zone\_vpcs](#input\_existing\_cbr\_zone\_vpcs) | Provide a existing zone id for VPC | <pre>object(<br>    {<br>      zone_id = string<br>  })</pre> | `null` | no |
| <a name="input_existing_serviceref_zone"></a> [existing\_serviceref\_zone](#input\_existing\_serviceref\_zone) | Provide a valid service reference and existing zone id | <pre>map(object(<br>    {<br>      zone_id = string<br>  }))</pre> | `{}` | no |
| <a name="input_kms_service_targeted_by_prewired_rules"></a> [kms\_service\_targeted\_by\_prewired\_rules](#input\_kms\_service\_targeted\_by\_prewired\_rules) | IBM Cloud offers two distinct Key Management Services (KMS): Key Protect and Hyper Protect Crypto Services (HPCS). This variable determines the specific KMS service to which the pre-configured rules will be applied. Use the value 'key-protect' to specify the Key Protect service, and 'hs-crypto' for the Hyper Protect Crypto Services (HPCS). | `list(string)` | <pre>[<br>  "hs-crypto"<br>]</pre> | no |
| <a name="input_location"></a> [location](#input\_location) | The region in which the network zone is scoped | `string` | `null` | no |
| <a name="input_prefix"></a> [prefix](#input\_prefix) | Prefix to append to all vpc\_zone\_list, service\_ref\_zone\_list and cbr\_rule\_description created by this submodule | `string` | n/a | yes |
| <a name="input_skip_specific_services_for_zone_creation"></a> [skip\_specific\_services\_for\_zone\_creation](#input\_skip\_specific\_services\_for\_zone\_creation) | Provide a list of service references for which zone creation is not required | `list(string)` | `[]` | no |
| <a name="input_target_service_details"></a> [target\_service\_details](#input\_target\_service\_details) | Details of the target service for which a rule is created. The key is the service name. | <pre>map(object({<br>    target_rg        = optional(string)<br>    instance_id      = optional(string)<br>    enforcement_mode = string<br>    tags             = optional(list(string))<br>  }))</pre> | `{}` | no |
| <a name="input_zone_service_ref_list"></a> [zone\_service\_ref\_list](#input\_zone\_service\_ref\_list) | (List) Service reference for the zone creation | `list(string)` | <pre>[<br>  "cloud-object-storage",<br>  "codeengine",<br>  "containers-kubernetes",<br>  "databases-for-cassandra",<br>  "databases-for-elasticsearch",<br>  "databases-for-enterprisedb",<br>  "databases-for-etcd",<br>  "databases-for-mongodb",<br>  "databases-for-mysql",<br>  "databases-for-postgresql",<br>  "databases-for-redis",<br>  "directlink",<br>  "iam-groups",<br>  "is",<br>  "messagehub",<br>  "messages-for-rabbitmq",<br>  "schematics",<br>  "secrets-manager",<br>  "server-protect",<br>  "user-management",<br>  "apprapp",<br>  "compliance",<br>  "event-notifications",<br>  "logdna",<br>  "logdnaat"<br>]</pre> | no |
| <a name="input_zone_vpc_crn_list"></a> [zone\_vpc\_crn\_list](#input\_zone\_vpc\_crn\_list) | (List) VPC CRN for the zones | `list(string)` | n/a | yes |

### Outputs

| Name | Description |
|------|-------------|
| <a name="output_account_id"></a> [account\_id](#output\_account\_id) | Account ID |
| <a name="output_map_service_ref_name_zoneid"></a> [map\_service\_ref\_name\_zoneid](#output\_map\_service\_ref\_name\_zoneid) | Map of service reference and zone ids |
| <a name="output_map_target_service_rule_ids"></a> [map\_target\_service\_rule\_ids](#output\_map\_target\_service\_rule\_ids) | Map of target service and rule ids |
| <a name="output_map_vpc_zoneid"></a> [map\_vpc\_zoneid](#output\_map\_vpc\_zoneid) | Map of VPC and zone ids |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
