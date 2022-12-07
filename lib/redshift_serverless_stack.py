
import aws_cdk.core as cdk
# from constructs import Construct

import aws_cdk.aws_redshiftserverless as redshiftserverless


class RedshiftServerlessStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "cdk-namespace"
        workgroup_name = "cdk-workgroup"

        namespace_configuration = {
            "namespace_name": namespace_name,
            "admin_username": "master",
            "admin_user_password": "xxx",
            "db_name": "lmh",
            "default_iam_role_arn": "xxx",
            "log_exports": ["useractivitylog"],
            "tags": [{"key": "type", "value": "lmh-20"}],
            "iam_roles": ["xxx"]
        }

        workgroup_configuration = {
            "namespace_name": namespace_name,
            "workgroup_name": workgroup_name,
            "publicly_accessible": False,
            "tags": [{"key": "type", "value": "lmh-20"}, ]
        }
        redshift_sls_namespace = redshiftserverless.CfnNamespace(
            self, "namespaceid", **namespace_configuration)
        redshift_sls_workgroup = redshiftserverless.CfnWorkgroup(
            self, "workgroupid", **workgroup_configuration)
