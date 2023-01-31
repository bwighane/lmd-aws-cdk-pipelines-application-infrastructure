
import aws_cdk.aws_redshiftserverless as redshiftserverless
import aws_cdk.core as cdk
import aws_cdk.aws_iam as iam


class RedshiftServerlessNamespaceStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        namespace_name = "lmd-v2"

        redshift_full_command_access = iam.ManagedPolicy.from_aws_managed_policy_name(
            "AmazonRedshiftAllCommandsFullAccess")

        role = iam.Role(self, "sls-test-role",
                        assumed_by=iam.ServicePrincipal("redshift.amazonaws.com"),
                        managed_policies=[redshift_full_command_access])

        namespace_configuration = {
            "namespace_name": namespace_name,
            "admin_username": "master",
            "admin_user_password": "xuL9cMx09#iE",
            "db_name": "liberia",
            "default_iam_role_arn": role.role_arn,
            "log_exports": ["useractivitylog"],
            "tags": [{"key": "type", "value": "lmd-2"}],
            "iam_roles": [role.role_arn]
        }

        redshift_sls_namespace = redshiftserverless.CfnNamespace(
            self, "namespaceid", **namespace_configuration)
