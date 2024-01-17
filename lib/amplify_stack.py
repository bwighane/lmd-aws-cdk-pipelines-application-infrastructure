import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_amplify as amplify
import aws_cdk.core as cdk

from .configuration import (
    DEPLOYMENT,
    AMPLIFY_GITHUB_REPOSITORY_NAME,
    GITHUB_REPOSITORY_OWNER_NAME,
    GITHUB_TOKEN,
    get_all_configurations,
)


class AmplifyStack(cdk.Stack):
    def __init__(
        self, scope: cdk.Construct, construct_id: str, target_environment: str, **kwargs
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        self.mappings = get_all_configurations()

        amplify_app = amplify.App(
            self,
            f"{target_environment}-app",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner=self.mappings[DEPLOYMENT][GITHUB_REPOSITORY_OWNER_NAME],
                repository=self.mappings[DEPLOYMENT][AMPLIFY_GITHUB_REPOSITORY_NAME],
                oauth_token=cdk.SecretValue.secrets_manager(
                    self.mappings[DEPLOYMENT][GITHUB_TOKEN]
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
        )
