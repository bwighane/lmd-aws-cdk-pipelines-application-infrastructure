import aws_cdk.core as cdk
from .tagging import tag
from .configuration import get_logical_id_prefix
from constructs import Construct
from .serverless_backend_stack import ServerlessBackendStack


class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, target_environment: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        logical_id_prefix = get_logical_id_prefix()

        service = ServerlessBackendStack(
            self,
            f"{target_environment}-serverless-backend",
            target_environment,
            **kwargs,
        )

        tag(service, target_environment)
