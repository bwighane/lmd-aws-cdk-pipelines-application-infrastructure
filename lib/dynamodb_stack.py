from aws_cdk import (
    Stack,
    aws_iam as iam,
    CfnOutput,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)
from constructs import Construct


class DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB table
        self.table = dynamodb.Table(
            self,
            f'DynamoTable-{target_environment}',
            partition_key=dynamodb.Attribute(
                name='id',
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,  # Use on-demand billing
            removal_policy=RemovalPolicy.DESTROY if target_environment != 'prod' else RemovalPolicy.RETAIN,
            point_in_time_recovery=True,  # Enable point-in-time recovery
            encryption=dynamodb.TableEncryption.AWS_MANAGED,  # Use AWS managed encryption
            table_name="portal_ui_useage_events"
        )

        # Output the table name and ARN
        CfnOutput(
            self,
            f'TableName-{target_environment}',
            value=self.table.table_name,
            description='DynamoDB table name'
        )

        CfnOutput(
            self,
            f'TableArn-{target_environment}',
            value=self.table.table_arn,
            description='DynamoDB table ARN'
        )

    # def get_github_connection(self):
    #     import boto3
    #     client = boto3.client('secretsmanager')
    #     secrets = []
    #     response = client.list_secrets()
    #     secrets.extend(response['SecretList'])
    #     while 'NextToken' in response:
    #         response = client.list_secrets(NextToken=response['NextToken'])
    #         secrets.extend(response['SecretList'])

    #     arn = next(
    #         secret for secret in secrets if 'github_arn' in secret['Name'].strip().lower())
    #     get_secret_value_response = client.get_secret_value(
    #         SecretId=arn['Name']
    #     )
    #     return get_secret_value_response['SecretString']
