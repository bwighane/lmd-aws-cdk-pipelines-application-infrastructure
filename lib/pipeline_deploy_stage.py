import aws_cdk.core as cdk
from .tagging import tag
from .configuration import get_logical_id_prefix
from constructs import Construct
from .lamda_gateway_stack import LambdaGatewayStack


class PipelineStage(cdk.Stage):
    def __init__(self, scope: Construct, id: str, target_environment: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        logical_id_prefix = get_logical_id_prefix()

        service = LambdaGatewayStack(
            self,
            f"{target_environment}{logical_id_prefix}LambdaGateway",
            target_environment=target_environment,
            **kwargs,
        )

        tag(service, target_environment)
