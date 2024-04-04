# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="lmd_aws_cdk_pipelines_application_infrastructure",
    version="0.0.2",
    description="A CDK Python app for deploying foundational infrastructure for Last Mile Data Portal in AWS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Branford T Gbieor <gbieorbranford@gmail.com>, Bwighane Mwalwanda <bsmwalwanda@gmail.com>",
    packages=setuptools.find_packages(),
    install_requires=[
        "aws-cdk-lib>=2.33.0",
        "constructs>=10.1.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
