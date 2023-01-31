
import aws_cdk.core as cdk
# from constructs import Construct

import aws_cdk.aws_redshiftserverless as redshiftserverless
from .redshift_serverless_namespace_stack import RedshiftServerlessNamespaceStack


class RedshiftServerlessWorkgroupStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "lmd-v2"
        workgroup_name = "lmd-v2"

        workgroup_configuration = {
            "namespace_name": namespace_name,
            "workgroup_name": workgroup_name,
            "publicly_accessible": True,
            "tags": [{"key": "type", "value": "lmd-2"}, ]
        }
        redshift_namespace_stack = RedshiftServerlessNamespaceStack(
            self,
            f'slsnspace',
            **kwargs,
        )
        self.add_dependency(redshift_namespace_stack)
        redshift_sls_workgroup = redshiftserverless.CfnWorkgroup(
            self, "workgroupid", **workgroup_configuration)
