import aws_cdk.core as cdk
from .tagging import tag
from .configuration import get_logical_id_prefix
from constructs import Construct
from .serverless_backend_stack import ServerlessBackendStack
from .amplify_stack import AmplifyStack


class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, target_environment: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        backend_service = ServerlessBackendStack(
            self,
            f"{target_environment}-serverless-backend",
            target_environment,
            **kwargs,
        )
        
        amplify_stack = AmplifyStack(
            self,
            f"{target_environment}-amplify",
            target_environment,
            **kwargs,
        )

        tag(backend_service, target_environment)
        tag(amplify_stack, target_environment)
