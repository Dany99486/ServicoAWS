import boto3
import json
from django.conf import settings

stepfunctions = boto3.client(
    'stepfunctions',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN,
    region_name=settings.AWS_REGION
)

def start_repair_workflow(input_data):
    return stepfunctions.start_execution(
        stateMachineArn=settings.STEP_FUNCTION_ARN,
        input=json.dumps(input_data)
    )
