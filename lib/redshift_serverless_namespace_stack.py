
import aws_cdk.aws_redshiftserverless as redshiftserverless
import aws_cdk.core as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_secretsmanager as secretsmanager
from .configuration import (REDSHIFT_DEFAULT_USER, REDSHIFT_DEFAULT_DATABASE)


class RedshiftServerlessNamespaceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = f"{target_environment}-lmd-v2".lower()

        redshift_full_command_access = iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonRedshiftAllCommandsFullAccess")

        role = iam.Role(self, f"{target_environment}LMDRedshiftServerlessRole",
                        assumed_by=iam.ServicePrincipal("redshift.amazonaws.com"),
                        managed_policies=[redshift_full_command_access])

        secret_string_generator = secretsmanager.SecretStringGenerator(
            include_space=False, exclude_punctuation=True, password_length=15, require_each_included_type=True, exclude_characters=" \\\"\/@")

        secret = secretsmanager.Secret(self, f'{target_environment}LMDRedshiftPassword',
                                       generate_secret_string=secret_string_generator)

        namespace_configuration = {
            "namespace_name": namespace_name,
            "admin_username": REDSHIFT_DEFAULT_USER,
            "admin_user_password": secret.secret_value.unsafe_unwrap(),
            "db_name": REDSHIFT_DEFAULT_DATABASE,
            "default_iam_role_arn": role.role_arn,
            "log_exports": ["useractivitylog"],
            "tags": [{"key": "type", "value": "lmd-2"}],
            "iam_roles": [role.role_arn]
        }

        redshift_sls_namespace = redshiftserverless.CfnNamespace(
            self, f'{target_environment}lmdnamespaceid'.lower(), **namespace_configuration)
