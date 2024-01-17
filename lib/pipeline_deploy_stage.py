import aws_cdk.core as cdk
from .tagging import tag
from constructs import Construct
from .serverless_backend_stack import ServerlessBackendStack
from .amplify_stack import AmplifyStack
from .cognito_stack import CognitoStack


class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, target_environment: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create the ServerlessBackendStack
        '''
        backend_service = ServerlessBackendStack(
            self,
            f"{target_environment}-serverless-backend",
            target_environment,
            **kwargs,
        )
        '''
        
        # Create the AmplifyStack
        amplify_stack = AmplifyStack(
            self,
            f"{target_environment}-amplify",
            target_environment,
            **kwargs,
        )
        
        cognito_stack = CognitoStack(
            self,
            f"{target_environment}-cognito",
            target_environment,
            **kwargs,
        )
        
        # Tag the backend_service and amplify_stack with the target_environment
        tag(cognito_stack, target_environment)
        tag(amplify_stack, target_environment)
