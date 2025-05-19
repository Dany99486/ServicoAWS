from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FaceRegisterSerializer, FaceLoginSerializer, RepairRequestSerializer
from .rekognition import add_face, search_face
from .dynamo import update_user_face_id, get_user_by_face_id, create_repair_request
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