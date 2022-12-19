
import aws_cdk.core as cdk
# from constructs import Construct

import aws_cdk.aws_redshiftserverless as redshiftserverless
from .redshift_serverless_namespace_stack import RedshiftServerlessNamespaceStack

from .configuration import (
    ACCOUNT_ID, DEPLOYMENT, DEV, TEST, PROD, REGION,
    get_logical_id_prefix, get_all_configurations
)


class RedshiftServerlessWorkgroupStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "lmd-2"
        workgroup_name = "lmd-2"

        target_environment = DEV
        logical_id_prefix = get_logical_id_prefix()

        workgroup_configuration = {
            "namespace_name": namespace_name,
            "workgroup_name": workgroup_name,
            "publicly_accessible": False,
            "tags": [{"key": "type", "value": "lmd-2"}, ]
        }
        redshift_namespace_stack = RedshiftServerlessNamespaceStack(
            self,
            f'rslsnspace',
            **kwargs,
        )
        self.add_dependency(redshift_namespace_stack)
        redshift_sls_workgroup = redshiftserverless.CfnWorkgroup(
            self, "workgroupid", **workgroup_configuration)
