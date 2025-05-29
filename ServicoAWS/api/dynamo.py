import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.conf import settings
from datetime import date, timedelta

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

    
def get_repair_request(user_id, request_id):
    table = dynamodb.Table('RepairRequests')
    response = table.get_item(Key={'user_id': user_id, 'request_id': request_id})
    return response.get('Item')

def get_appointments_for_next_week():
    table = dynamodb.Table('Appointments')
    today = date.today()
    all_available = []

    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.isoformat()

        response = table.query(
            KeyConditionExpression=Key('date').eq(date_str)
        )
        slots = response.get('Items', [])
        available_slots = [s['time_slot'] for s in slots if s.get('is_available')]

        all_available.append({
            "date": date_str,
            "available_slots": available_slots
        })

    return all_available

def get_appointments_from_today_flat():
    table = dynamodb.Table('Appointments')
    today = date.today().isoformat()  # Converte a data para uma string no formato ISO
    response = table.scan(
        FilterExpression=Attr('date').gte(today)
    )
    slots = response.get('Items', [])
    slots_sorted = sorted(slots, key=lambda x: (x['date'], x['time_slot']))

    return slots_sorted

def get_all_repairs():
    table = dynamodb.Table('RepairRequests')
    response = table.scan()
    repairs = response.get('Items', [])
    repairs_sorted = sorted(repairs, key=lambda x: (x['appointment_date'], x['time_slot']))

    return repairs_sorted

def get_all_users():
    table = dynamodb.Table('Users')
    response = table.scan()
    users = response.get('Items', [])
    users_sorted = sorted(users, key=lambda x: x['user_id'])

    return users_sorted