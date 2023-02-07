
import aws_cdk.aws_redshiftserverless as redshiftserverless
import aws_cdk.core as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_secretsmanager as secretsmanager
from .configuration import (REDSHIFT_DEFAULT_USER, REDSHIFT_DEFAULT_DATABASE)


class RedshiftServerlessNamespaceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "lmd-v2"

        redshift_full_command_access = iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonRedshiftAllCommandsFullAccess")

        role = iam.Role(self, "LMD20RedshiftServerlessRole",
                        assumed_by=iam.ServicePrincipal("redshift.amazonaws.com"),
                        managed_policies=[redshift_full_command_access])

        secret = secretsmanager.Secret(self, "LMD20RedshiftPassword")

        namespace_configuration = {
            "namespace_name": namespace_name,
            "admin_username": REDSHIFT_DEFAULT_USER,
            "admin_user_password": secret.secret_value.unsafe_plain_text(),
            "db_name": REDSHIFT_DEFAULT_DATABASE,
            "default_iam_role_arn": role.role_arn,
            "log_exports": ["useractivitylog"],
            "tags": [{"key": "type", "value": "lmd-2"}],
            "iam_roles": [role.role_arn]
        }

        redshift_sls_namespace = redshiftserverless.CfnNamespace(
            self, "namespaceid", **namespace_configuration)
