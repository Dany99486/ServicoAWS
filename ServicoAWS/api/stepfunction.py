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

def send_approval_result(task_token, aprovado):
    if aprovado:
        stepfunctions.send_task_success(
            taskToken=task_token,
            output=json.dumps({'aprovado': True})
        )
    else:
        stepfunctions.send_task_failure(
            taskToken=task_token,
            error='ClienteNaoAprovou',
            cause='Cliente recusou o orçamento.'
        )

def send_present_result(task_token, present):
    if present:
        stepfunctions.send_task_success(
            taskToken=task_token,
            output=json.dumps({'presente': True})
        )
    else:
        stepfunctions.send_task_failure(
            taskToken=task_token,
            error='ClienteNaoPresente',
            cause='Cliente não estava presente na data agendada.'
        )
        
def send_repair_result(task_token):
    stepfunctions.send_task_success(
        taskToken=task_token,
        output=json.dumps({'reparo_concluido': True})
    )
    
def send_pagamento_result(task_token):
    stepfunctions.send_task_success(
        taskToken=task_token,
        output=json.dumps({"pagamento_confirmado": True})
    )
    
def send_recolha_result(task_token):
    stepfunctions.send_task_success(
        taskToken=task_token,
        output=json.dumps({"equipamento_recolhido": True})
    )