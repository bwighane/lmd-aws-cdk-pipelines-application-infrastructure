import aws_cdk.core as cdk
import aws_cdk.aws_cognito as cognito


from .configuration import (
    DEPLOYMENT,
    COGNITO_CALLBACK_URLS,
    COGNITO_LOGOUT_URLS,
    get_all_configurations,
)

class CognitoStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str,target_environment: str, **kwargs) -> None:
            """
            Initializes a new instance of the CognitoStack class.

            Args:
                scope (core.Construct): The parent construct.
                id (str): The ID of the construct.
                target_environment (str): The target environment.
                **kwargs: Additional keyword arguments.

            Returns:
                None
            """
            super().__init__(scope, id, **kwargs)
            
            self.mappings = get_all_configurations()

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
                )
            )

            user_pool_client = user_pool.add_client(f'{id}-user-pool-client',
                generate_secret=True,
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
