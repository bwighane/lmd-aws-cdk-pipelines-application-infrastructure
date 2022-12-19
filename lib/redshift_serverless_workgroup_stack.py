
import aws_cdk.core as cdk
# from constructs import Construct

import aws_cdk.aws_redshiftserverless as redshiftserverless


class RedshiftServerlessWorkgroupStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "lmd-2"
        workgroup_name = "lmd-2"

        workgroup_configuration = {
            "namespace_name": namespace_name,
            "workgroup_name": workgroup_name,
            "publicly_accessible": False,
            "tags": [{"key": "type", "value": "lmd-2"}, ]
        }

        redshift_sls_workgroup = redshiftserverless.CfnWorkgroup(
            self, "workgroupid", **workgroup_configuration)
