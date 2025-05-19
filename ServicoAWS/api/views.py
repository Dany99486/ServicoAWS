from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FaceRegisterSerializer, FaceLoginSerializer, RepairRequestSerializer
from .rekognition import add_face, search_face
from .dynamo import update_user_face_id, get_user_by_face_id, create_repair_request, get_appointments_for_next_week
from .authentication import get_user_id_from_request
from .stepfunction import start_repair_workflow
import jwt
from django.conf import settings

from uuid import uuid4

class FaceRegisterView(APIView):
    def post(self, request):
        serializer = FaceRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            user_id = data['user_id']
            image = data['image'].read()

            face_id = add_face(user_id, image)
            if not face_id:
                return Response({'error': 'No face detected'}, status=400)

            update_user_face_id(user_id, face_id)
            return Response({'message': 'Face registered', 'user_id': user_id, 'face_id': face_id})
        return Response(serializer.errors, status=400)



class FaceLoginView(APIView):
    def post(self, request):
        serializer = FaceLoginSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image'].read()
            face_id = search_face(image)

            if not face_id:
                return Response({'error': 'Face not recognized'}, status=401)

            user = get_user_by_face_id(face_id)
            if not user:
                return Response({'error': 'User not found'}, status=404)

            token = jwt.encode({'user_id': user['user_id']}, settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token})
        return Response(serializer.errors, status=400)

class CreateRepairRequestView(APIView):
    def post(self, request):
        user_id = get_user_id_from_request(request)

        serializer = RepairRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            request_id = str(uuid4())

            # Gravar no Dynamo e iniciar Step Function
            create_repair_request(user_id, request_id, data)
            response = start_repair_workflow({
                "user_id": user_id,
                "request_id": request_id,
                "service_type": data['service_type'],
                "appointment_date": str(data['appointment_date'])
            })

            return Response({
                "message": "Pedido iniciado",
                "executionArn": response['executionArn'],
                "request_id": request_id
            })
        return Response(serializer.errors, status=400)
    
from .dynamo import get_repair_request
from .serializers import RepairStatusSerializer
from .authentication import get_user_id_from_request

class RepairStatusView(APIView):
    def get(self, request):
        user_id = get_user_id_from_request(request)
        serializer = RepairStatusSerializer(data=request.data)
        if serializer.is_valid():
            request_id = serializer.validated_data['request_id']
            item = get_repair_request(user_id, request_id)
            if item:
                return Response({
                    "status": item.get("status", "desconhecido"),
                    "data": item
                })
            return Response({"error": "Pedido não encontrado"}, status=404)
        return Response(serializer.errors, status=400)

class ShopInfoView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        upcoming_slots = get_appointments_for_next_week()

        shop_info = {
            "services": [
                {"type": "screen_replacement", "price": 100.0, "duration_minutes": 90},
                {"type": "virus_removal", "price": 50.0, "duration_minutes": 60},
                {"type": "battery_replacement", "price": 80.0, "duration_minutes": 45}
            ],
            "working_hours": {
                "weekdays": "09:00 - 18:00",
                "saturday": "10:00 - 14:00",
                "sunday": "Closed"
            },
            "available_slots": upcoming_slots,
            "location": {
                "address": "Rua Exemplo 123, Lisboa",
                "contact": "+351 912 345 678",
                "email": "suporte@primetech.pt"
            }
        }

        return Response(shop_info)