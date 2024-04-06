import aws_cdk as cdk
import constructs as Construct
from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_elasticbeanstalk as elasticbeanstalk,
    aws_iam as iam,
    Stack,
)

from .configuration import (
    DEPLOYMENT, SERVICE_GITHUB_REPOSITORY_NAME, GITHUB_REPOSITORY_OWNER_NAME, GITHUB_TOKEN, get_all_configurations
)


class BeanstalkStack(Stack):
    def __init__(self, scope: Construct, id: str, target_environment: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.mappings = get_all_configurations()
        self.create_beanstalk_pipeline(
            target_environment,
        )

    def create_beanstalk_pipeline(self, target_environment):

        source_artifact = codepipeline.Artifact()

        # Create an Elastic Beanstalk application
        application = elasticbeanstalk.CfnApplication(
            self, f'{id}-portal-services',
            application_name=f'{target_environment}-portal-services',
        )

        # Create an Elastic Beanstalk environment
        environment = elasticbeanstalk.CfnEnvironment(
            self, f'{id}-portal-services-environment',
            application_name=application.application_name,
            environment_name=f'{target_environment}-portal-services-environment',
            solution_stack_name="64bit Amazon Linux 2023 v4.0.10 running Python 3.9",
        )

        # build_spec=codebuild.BuildSpec.from_object({
        #             "version": "0.2",
        #             "phases": {
        #                 "install": {
        #                     "runtime-versions": {
        #                         "python": "3.9"
        #                     },
        #                     "commands": [
        #                         "pip install -r requirements.txt"
        #                     ]
        #                 },
        #                 "build": {
        #                     "commands": [
        #                         "echo Build started on `date`",
        #                         "python build.py"
        #                     ]
        #                 }
        #             },
        #             "artifacts": {

        #                 "files": [
        #                     "build/**/*"
        #                 ]
        #             }
        #         }),
        # Create a CodeBuild project
        project = codebuild.PipelineProject(
            self, f'{id}-codebuild',
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "install": {
                        "runtime-versions": {
                            "python": "3.9"
                        },
                        "commands": [
                            "pip install -r requirements.txt"
                        ]
                    }
                },
                "artifacts": {
                    "type": "zip",
                    "files": [
                        "**/*"
                    ]
                }
            }),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_4_0,
                privileged=True
            )
        )

        # Grant necessary permissions to the CodeBuild project
        project.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "elasticbeanstalk:*",
                "s3:*",
                "cloudformation:*",
                "codedeploy:*",
                "codebuild:*",
                "codepipeline:*",
                "iam:PassRole"
            ],
            resources=["*"]
        ))

        # Create a CodePipeline pipeline
        app_pipeline = codepipeline.Pipeline(
            self, f'{id}-pipeline',
            pipeline_name=f'{target_environment}-pipeline',
            cross_account_keys=True,
        )

        # Add stages to the pipeline
        source_stage = codepipeline.StageProps(
            stage_name="Source",
            actions=[
                codepipeline_actions.GitHubSourceAction(
                    action_name="GitHub_Source",
                    owner=self.mappings[DEPLOYMENT][GITHUB_REPOSITORY_OWNER_NAME],
                    repo=self.mappings[DEPLOYMENT][SERVICE_GITHUB_REPOSITORY_NAME],
                    branch='main',  # hardcoding this for now, it will have to be dynamic to fit other accts.
                    oauth_token=cdk.SecretValue.secrets_manager(
                        self.mappings[target_environment][GITHUB_TOKEN]),
                    output=source_artifact
                )
            ]
        )

        build_stage = codepipeline.StageProps(
            stage_name="Build",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="CodeBuild",
                    project=project,
                    input=source_stage.actions[0].action_properties.outputs[0],
                    outputs=[codepipeline.Artifact()]
                )
            ]
        )

        deploy_stage = codepipeline.StageProps(
            stage_name="Deploy",
            actions=[
                codepipeline_actions.ElasticBeanstalkDeployAction(
                    action_name="ElasticBeanstalk_Deploy",
                    application_name=application.ref,
                    environment_name=environment.ref,
                    input=build_stage.actions[0].action_properties.outputs[0],
                )
            ]
        )

        app_pipeline.add_stage(stage_name=source_stage.stage_name, actions=source_stage.actions)
        app_pipeline.add_stage(stage_name=build_stage.stage_name, actions=build_stage.actions)
        app_pipeline.add_stage(stage_name=deploy_stage.stage_name, actions=deploy_stage.actions)
