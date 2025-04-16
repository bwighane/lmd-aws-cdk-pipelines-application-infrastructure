from aws_cdk import (
    Stack,
    aws_iam as iam,
    CfnOutput
)
import aws_cdk.aws_apprunner_alpha as apprunner
from constructs import Construct
from .configuration import SERVICE_GITHUB_REPOSITORY_NAME, GITHUB_REPOSITORY_OWNER_NAME


class AppRunnerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for App Runner service
        instance_role = iam.Role(
            self, "AppRunnerInstanceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com")
        )

        branch = "main" if target_environment.lower() == "dev" else target_environment.lower()

        # Add permissions to the role as needed
        instance_role.add_managed_policy(
            iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "ECRAccess",
                "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
            )
        )

        # Create an IAM policy for Secrets Manager access
        secrets_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "secretsmanager:ListSecrets",
                "secretsmanager:GetSecretValue"
            ],
            resources=["*"]  # You can restrict this to specific secret ARNs for better security
        )

        # Add the policy to your instance role
        instance_role.add_to_policy(secrets_policy)

        # Define environment variables
        environment_variables = {
            # Add sensitive variables that should be managed through environment
            "AWS_ACCESS_KEY_ID": "",
            "AWS_SECRET_ACCESS_KEY": "",
            "DB_ENGINE": "",
            "DB_HOST": "",
            "DB_NAME": "",
            "DB_PASS": "",
            "DB_PORT": "",
            "DB_USERNAME": "",
            "S3_UPLOAD_BUCKET": "",
        }

        # Create runtime configuration with environment variables
        runtime_config = apprunner.CodeConfigurationValues(
            runtime=apprunner.Runtime.PYTHON_3,
            build_command="pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt",
            start_command="gunicorn --config gunicorn-cfg.py application:application",
            port="5005",
            environment_variables=environment_variables
        )

        # Create an App Runner service
        service = apprunner.Service(
            self, "AppRunnerService",
            service_name="lmd-portal-services-cdk",

            # Configure the source with runtime configuration
            source=apprunner.Source.from_git_hub(
                # Replace with your repo
                repository_url=f"https://github.com/{GITHUB_REPOSITORY_OWNER_NAME}/{SERVICE_GITHUB_REPOSITORY_NAME}",
                branch=branch,  # Specify your branch
                configuration_source=apprunner.ConfigurationSourceType.API,
                code_configuration_values=runtime_config,
                connection=apprunner.GitHubConnection.from_connection_arn(
                    self.get_github_connection()
                )
            ),
            instance_role=instance_role,
            cpu=apprunner.Cpu.QUARTER_VCPU,
            memory=apprunner.Memory.ONE_GB,
            # Auto deployments for new commits
            auto_deployments_enabled=True
        )

        # Output the service URL
        CfnOutput(
            self, "ServiceUrl",
            value=service.service_url,
            description="App Runner Service URL"
        )

    def get_github_connection(self):
        import boto3
        client = boto3.client('secretsmanager')
        secrets = []
        response = client.list_secrets()
        secrets.extend(response['SecretList'])
        while 'NextToken' in response:
            response = client.list_secrets(NextToken=response['NextToken'])
            secrets.extend(response['SecretList'])

        arn = next(
            secret for secret in secrets if 'github_arn' in secret['Name'].strip().lower())
        get_secret_value_response = client.get_secret_value(
            SecretId=arn['Name']
        )
        return get_secret_value_response['SecretString']
