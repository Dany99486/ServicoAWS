import boto3
from django.conf import settings

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN,  # <-- aqui o token temporário
    region_name=settings.AWS_REGION
)

users_table = dynamodb.Table('Users')

def update_user_face_id(user_id, face_id):
    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET face_id = :f',
        ExpressionAttributeValues={':f': face_id}
    )

def get_user_by_face_id(face_id):
    response = users_table.scan(
        FilterExpression='face_id = :f',
        ExpressionAttributeValues={':f': face_id}
    )
    items = response.get('Items', [])
    return items[0] if items else None

def create_repair_request(user_id, request_id, data):
    table = dynamodb.Table('RepairRequests')
    table.put_item(
        Item={
            'user_id': user_id,
            'request_id': request_id,
            'service_type': data['service_type'],
            'appointment_date': str(data['appointment_date']),
            'status': 'iniciado'
        }
    )