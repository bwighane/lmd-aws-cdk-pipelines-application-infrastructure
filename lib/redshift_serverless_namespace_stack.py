
import aws_cdk.core as cdk
# from constructs import Construct

import aws_cdk.aws_redshiftserverless as redshiftserverless


class RedshiftServerlessNamespaceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "lmd-v2"

        namespace_configuration = {
            "namespace_name": namespace_name,
            "admin_username": "master",
            "admin_user_password": "xuL9cMx09#iE",
            "db_name": "liberia",
            "default_iam_role_arn": "arn:aws:iam::002190277880:role/service-role/AmazonRedshift-CommandsAccessRole-20221018T164627",
            "log_exports": ["useractivitylog"],
            "tags": [{"key": "type", "value": "lmd-2"}],
            "iam_roles": ["arn:aws:iam::002190277880:role/service-role/AmazonRedshift-CommandsAccessRole-20221018T164627"]
        }

        redshift_sls_namespace = redshiftserverless.CfnNamespace(
            self, "namespaceid", **namespace_configuration)
