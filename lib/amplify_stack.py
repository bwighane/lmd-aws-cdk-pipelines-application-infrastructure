from aws_cdk import Stack, SecretValue
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_amplify_alpha as amplify_alpha  # amplify is being updated constantly
from constructs import Construct

from .configuration import (
    DEPLOYMENT,
    AMPLIFY_GITHUB_REPOSITORY_NAME,
    GITHUB_REPOSITORY_OWNER_NAME,
    AMPLIFY_GITHUB_TOKEN,
    get_all_configurations,
)


class AmplifyStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, target_environment: str, **kwargs
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        self.mappings = get_all_configurations()

        amplify_app = amplify_alpha.App(
            self,
            f"{target_environment}-app",
            platform=amplify_alpha.Platform.WEB_COMPUTE,
            source_code_provider=amplify_alpha.GitHubSourceCodeProvider(
                owner=self.mappings[DEPLOYMENT][GITHUB_REPOSITORY_OWNER_NAME],
                repository=self.mappings[DEPLOYMENT][AMPLIFY_GITHUB_REPOSITORY_NAME],
                oauth_token=SecretValue.secrets_manager(
                    self.mappings[target_environment][AMPLIFY_GITHUB_TOKEN]
                ),
            ),
            build_spec=codebuild.BuildSpec.from_object_to_yaml(
                {
                    # Alternatively add a `amplify.yml` to the repo
                    "version": "1.0",
                    "frontend": {
                        "phases": {
                            "pre_build": {"commands": ["npm install --legacy-peer-deps"]},
                            "build": {"commands": ["npm run build"]},
                        },
                        "artifacts": {"base_directory": ".next", "files": "**/*"},
                        "cache": {"paths": "node_modules/**/*"},
                    },
                }
            ),
            platform=amplify_alpha.Platform.WEB_COMPUTE



        )
