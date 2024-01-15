import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError
import logging

s3 = boto3.client("s3")
dynamodb = boto3.client("dynamodb")

table = os.environ["table"]
bucket = os.environ["bucket"]

def upload_metadata(key, file_id):
    reference = {"Bucket": {"S": bucket}, "Key": {"S": key}}
    response = dynamodb.put_item(
        TableName=table,
        Item={"file_id": {"S": file_id}, "file_reference": {"M": reference}},
    )
    print(response)


def upload_file_to_s3(file_name, bucket, object_name=None):

    file_id = str(uuid.uuid4())
    key = str(uuid.uuid4()) # I need to define a valid s3 key here
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3.upload_file(file_name, bucket, object_name)
        upload_metadata(key, file_id)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def handler(event, context):
    print(event)

    data = json.loads(event["body"])
    file_name = data["file_name"]

    if upload_file_to_s3(file_name, bucket):
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps("Success!"),
        }
    return {
        "statusCode": 500,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps("Request Failed!"),
    }
