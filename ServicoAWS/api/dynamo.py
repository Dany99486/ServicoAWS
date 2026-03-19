import boto3
from boto3.dynamodb.conditions import Key, Attr
from django.conf import settings
from datetime import date, timedelta
from datetime import datetime

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

ALL_POSSIBLE_SLOTS = [
    "09:00-10:00", "10:00-11:00", "11:00-12:00",
    "13:00-14:00", "14:00-15:00", "15:00-16:00",
    "16:00-17:00", "17:00-18:00"
]

def get_appointments_for_next_week():
    table = dynamodb.Table('Appointments')
    today = date.today()
    all_available = []

    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.isoformat()

        # Consulta os horários já reservados para essa data
        response = table.query(
            KeyConditionExpression=Key('date').eq(date_str)
        )
        items = response.get('Items', [])

        # Extrai os horários que já estão ocupados
        reserved_slots = [item['time_slot'] for item in items]

        # Horários disponíveis = todos - reservados
        available_slots = [
            slot for slot in ALL_POSSIBLE_SLOTS if slot not in reserved_slots
        ]

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

def get_appointments_by_user(user_id):
    table = dynamodb.Table('RepairRequests')
    
    try:
        # Usamos query pois temos a partition key
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        
        appointments = response.get('Items', [])

        print("Appointments brutos:", appointments)  # Debug opcional

        # Filtra os que não estão disponíveis
        filtered_appointments = [
            item for item in appointments 
            if item.get('status') != 'disponivel'
        ]
        
        # Ordena por data e hora, com fallback de data inválida
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
            except Exception:
                return datetime.min

        sorted_appointments = sorted(
            filtered_appointments,
            key=lambda x: (
                parse_date(x.get('appointment_date', '1970-01-01 00:00:00+00:00')),
                x.get('time_slot', '')
            )
        )
        
        return {
            "user_id": user_id,
            "appointments": sorted_appointments
        }
    
    except Exception as e:
        print(f"Erro ao buscar agendamentos: {str(e)}")
        return {
            "user_id": user_id,
            "appointments": [],
            "error": str(e)
        }