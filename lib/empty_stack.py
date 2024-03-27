# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import Stack
from constructs import Construct


class EmptyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        This stack is intentionally left empty. This is used during bootstrap to prevent synth of
        stacks that are dependend on configuration.

        @param scope cdk.Construct: Parent of this stack, usually an App or a Stage, but could be any construct.:
        @param construct_id str:
            The construct ID of this stack. If stackName is not explicitly defined,
            this id (and any parent IDs) will be used to determine the physical ID of the stack.
        @param kwargs:
        """
        super().__init__(scope, construct_id, **kwargs)
        pass
