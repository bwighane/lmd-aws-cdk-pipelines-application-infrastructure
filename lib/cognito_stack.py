from aws_cdk import Stack
from constructs import Construct

from aws_cdk import aws_cognito as cognito

from .configuration import (
    DEPLOYMENT,
    COGNITO_CALLBACK_URLS,
    COGNITO_LOGOUT_URLS,
    ADMIN_EMAIL,
    get_all_configurations,
)


class CognitoStack(Stack):
    def __init__(self, scope: Construct, id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.mappings = get_all_configurations()
        self.cognito_authenticate(target_environment)

    def cognito_authenticate(self, target_environment):

        # Create a UserPool
        user_pool = cognito.UserPool(self, f'{id}-user-pool',
                                     user_pool_name=f'{target_environment}-user-pool',
                                     self_sign_up_enabled=True,
                                     auto_verify=cognito.AutoVerifiedAttrs(email=True),
                                     password_policy=cognito.PasswordPolicy(
            min_length=8,
            require_lowercase=True,
            require_uppercase=True,
            require_digits=True,
            require_symbols=True
        ),
            email=cognito.UserPoolEmail.with_ses(
                from_email=ADMIN_EMAIL,
                reply_to=ADMIN_EMAIL,
        )
        )

        # Create a UserPool Client
        user_pool_client = user_pool.add_client(f'{id}-user-pool-client',
                                                prevent_user_existence_errors=True,
                                                o_auth=cognito.OAuthSettings(
            flows=cognito.OAuthFlows(
                authorization_code_grant=True,
                implicit_code_grant=True
            ),
            scopes=[
                cognito.OAuthScope.EMAIL,
                cognito.OAuthScope.OPENID,
                cognito.OAuthScope.PROFILE
            ],
            callback_urls=[self.mappings[DEPLOYMENT][COGNITO_CALLBACK_URLS]],
            logout_urls=[self.mappings[DEPLOYMENT][COGNITO_LOGOUT_URLS]]
        )
        )
