from constructs import Construct
import aws_cdk.core as cdk
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_apigateway as apigw

class LambdaGatewayStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=my_lambda,
        )