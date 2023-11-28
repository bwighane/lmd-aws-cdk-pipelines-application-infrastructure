import aws_cdk.core as cdk
import aws_cdk.aws_cognito as _cognito
import aws_cdk.aws_s3 as _s3
import aws_cdk.aws_dynamodb as _dynamodb
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_apigateway as _apigateway
import aws_cdk.aws_rds as rds
import aws_cdk.aws_ec2 as ec2


from .configuration import (
    S3_UPLOAD_BUCKET,
    VPC_CIDR,
    get_environment_configuration,
    get_logical_id_prefix,
)

from constructs import Construct
import os


class ServerlessBackendStack(cdk.Stack):
    def __init__(
        self, scope: Construct, construct_id: str, target_environment: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.target_environment = target_environment
        mappings = get_environment_configuration(target_environment)
        logical_id_prefix = get_logical_id_prefix()
        
        mappings = get_environment_configuration(target_environment)
        vpc_cidr = mappings[VPC_CIDR]
        logical_id_prefix = get_logical_id_prefix()
        vpc = ec2.Vpc(self, f'{logical_id_prefix}Vpc', cidr=vpc_cidr)
        
        vpc.add_gateway_endpoint(
            f'{target_environment}{logical_id_prefix}S3Endpoint',
            service=ec2.GatewayVpcEndpointAwsService.S3
        )
        vpc.add_gateway_endpoint(
            f'{target_environment}{logical_id_prefix}DynamoEndpoint',
            service=ec2.GatewayVpcEndpointAwsService.DYNAMODB
        )

        user_pool = _cognito.UserPool(
            self, f"{target_environment}{logical_id_prefix}UserPool"
        )
        
        user_pool.add_client(
            f"{target_environment}{logical_id_prefix}app-client",
            auth_flows=_cognito.AuthFlow(user_password=True),
            supported_identity_providers=[
                _cognito.UserPoolClientIdentityProvider.COGNITO
            ],
        )
        
        auth = _apigateway.CognitoUserPoolsAuthorizer(
            self, f"{target_environment}{logical_id_prefix}authorizer", cognito_user_pools=[user_pool]
        )

        file_upload_meta_table = _dynamodb.Table(
            self,
            id=f"{logical_id_prefix}metadata",
            table_name="data_upload_metadata",
            partition_key=_dynamodb.Attribute(
                name="file_id", type=_dynamodb.AttributeType.STRING
            ),
        )  # change primary key here

        upload_bucket = _s3.Bucket(
            self, id=f"{logical_id_prefix}uploads3bucket", bucket_name=mappings[S3_UPLOAD_BUCKET].lower()
        )

        file_upload_lambda = _lambda.Function(
            self,
            id=f"{logical_id_prefix}fileuploadfunction",
            function_name="fileuploadfunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="index.handler",
            code=_lambda.Code.from_asset(os.path.join("./", "lambda")),
            environment={"bucket": upload_bucket.bucket_name, "table": file_upload_meta_table.table_name},
        )
        
        engine_version = rds.MysqlEngineVersion.VER_8_0_28
        instance_type = ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO)

        rds_instance = rds.DatabaseInstance(
            self,
            f"{logical_id_prefix}MySqlInstance",
            database_name=f"{logical_id_prefix}applicationDBinstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=engine_version),
            instance_type=instance_type,
            vpc=vpc,
            port=3306,
            deletion_protection=False,
        )

        upload_bucket.grant_read_write(file_upload_lambda)
        file_upload_meta_table.grant_read_write_data(file_upload_lambda)
        
        file_upload_api = _apigateway.LambdaRestApi(
            self, id="uploadapi", rest_api_name="fileuploadapi", handler=file_upload_lambda, proxy=True
        )
        
        postData = file_upload_api.root.add_resource("form")
        postData.add_method(
            "POST",
            authorizer=auth,
            authorization_type=_apigateway.AuthorizationType.COGNITO,
        )  # POST files & metadata
