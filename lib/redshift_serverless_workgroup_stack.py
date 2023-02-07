
import aws_cdk.core as cdk
# from constructs import Construct

import aws_cdk.aws_redshiftserverless as redshiftserverless
from .redshift_serverless_namespace_stack import RedshiftServerlessNamespaceStack


class RedshiftServerlessWorkgroupStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = f"{target_environment}-lmd-v2".lower()
        workgroup_name = f"{target_environment}-lmd-v2".lower()

        workgroup_configuration = {
            "namespace_name": namespace_name,
            "workgroup_name": workgroup_name,
            "publicly_accessible": True,
            "tags": [{"key": "type", "value": "lmd-2"}]
        }
        redshift_namespace_stack = RedshiftServerlessNamespaceStack(
            self,
            f'{target_environment}rednspace'.lower(),
            target_environment,
            **kwargs,
        )
        self.add_dependency(redshift_namespace_stack)
        redshift_sls_workgroup = redshiftserverless.CfnWorkgroup(
            self, f'{target_environment}lmdworkgroupid'.lower(), **workgroup_configuration)
