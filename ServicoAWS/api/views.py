from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientApprovalSerializer, ConfirmarPagamentoSerializer, ConfirmarPresencaSerializer, ConfirmarRecolhaSerializer, FaceRegisterSerializer, FaceLoginSerializer, RepairRequestSerializer, RepairStatusSerializer, StaffConcluiReparacaoSerializer
from .rekognition import add_face, search_face
from .dynamo import get_appointments_by_user, update_user_face_id, get_user_by_face_id, get_appointments_for_next_week, get_repair_request, get_appointments_from_today_flat, get_all_repairs, get_all_users
from .authentication import get_user_id_from_request
from .stepfunction import send_approval_result, send_pagamento_result, send_present_result, send_recolha_result, send_repair_result, start_repair_workflow
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

            # 1. Preparar dados para a Step Function, incluindo o cartão
            input_data = {
                "user_id": user_id,
                "request_id": request_id,
                "service_type": data['service_type'],
                "appointment_date": str(data['appointment_date']),
                "time_slot": data['time_slot']
                #"card": data['card']  # novo: cartão incluído
            }

            # 2. Inicia a Step Function
            response = start_repair_workflow(input_data)

            return Response({
                "message": "Pedido submetido com sucesso",
                "request_id": request_id,
                "executionArn": response['executionArn']
            })

        return Response(serializer.errors, status=400)
    
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

class ClientApprovalView(APIView):
    def post(self, request):
        user_id = get_user_id_from_request(request)
        serializer = ClientApprovalSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        request_id = str(serializer.validated_data['request_id'])
        aprovado = serializer.validated_data['aprovado']

        # Buscar o pedido
        item = get_repair_request(user_id, request_id)
        if not item:
            return Response({'error': 'Pedido não encontrado'}, status=404)

        task_token = item.get('approval_task_token')
        if not task_token:
            return Response({'error': 'Token de aprovação não encontrado'}, status=500)

        # Enviar resultado para Step Function
        try:
            send_approval_result(task_token, aprovado, user_id, request_id)
        except Exception as e:
            return Response({'error': f'Erro ao enviar para Step Function: {str(e)}'}, status=500)

        return Response({'message': 'Resposta enviada com sucesso para a Step Function'})

class StaffConfirmarPresencaView(APIView):
    def post(self, request):
        serializer = ConfirmarPresencaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user_id = serializer.validated_data['user_id']
        request_id = serializer.validated_data['request_id']
        presente = serializer.validated_data['presente']

        item = get_repair_request(user_id, request_id)
        if not item:
            return Response({'error': 'Pedido não encontrado'}, status=404)

        task_token = item.get('presenca_task_token')
        if not task_token:
            return Response({'error': 'Token de presença não encontrado'}, status=500)

        try:
            send_present_result(task_token, presente, user_id, request_id, item.get('service_type'))
        except Exception as e:
            return Response({'error': f'Erro ao comunicar com Step Function: {str(e)}'}, status=500)

        return Response({'message': 'Presença processada com sucesso'})

class ConfirmarPagamentoFinalView(APIView):
    def post(self, request):
        serializer = ConfirmarPagamentoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user_id = get_user_id_from_request(request)
        request_id = serializer.validated_data['request_id']

        item = get_repair_request(user_id, request_id)
        if not item:
            return Response({'error': 'Pedido não encontrado'}, status=404)

        task_token = item.get('pagamento_task_token')
        if not task_token:
            return Response({'error': 'Token de pagamento não encontrado'}, status=500)

        try:
            send_pagamento_result(task_token, user_id, request_id)
        except Exception as e:
            return Response({'error': f'Erro ao enviar para Step Function: {str(e)}'}, status=500)

        return Response({'message': 'Pagamento confirmado com sucesso'})
    
class ConfirmarRecolhaView(APIView):
    def post(self, request):
        serializer = ConfirmarRecolhaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user_id = serializer.validated_data['user_id']
        request_id = serializer.validated_data['request_id']

        item = get_repair_request(user_id, request_id)
        if not item:
            return Response({'error': 'Pedido não encontrado'}, status=404)

        task_token = item.get('recolha_task_token')
        if not task_token:
            return Response({'error': 'Token de recolha não encontrado'}, status=500)

        try:
            send_recolha_result(task_token, user_id, request_id)
        except Exception as e:
            return Response({'error': f'Erro ao enviar para Step Function: {str(e)}'}, status=500)

        return Response({'message': 'Recolha confirmada com sucesso'})
    
class StaffConcluiReparacaoView(APIView):
    def post(self, request):
        serializer = StaffConcluiReparacaoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        user_id = serializer.validated_data['user_id']
        request_id = serializer.validated_data['request_id']
        
        item = get_repair_request(user_id, request_id)
        if not item:
            return Response({'error': 'Pedido não encontrado'}, status=404)
        
        task_token = item.get('conclusao_task_token')
        if not task_token:
            return Response({'error': 'Token de conclusão não encontrado'}, status=500)
        
        try:
            send_repair_result(task_token, user_id, request_id)
        except Exception as e:
            return Response({'error': f'Erro ao comunicar com Step Function: {str(e)}'}, status=500)
        
        return Response({'message': 'Reparação concluída com sucesso'})
    
class AppointmentsListView(APIView):
    def get(self, request):
        try:
            appointments = get_appointments_from_today_flat()
            if not appointments:
                return Response(
                    {"message": "Não há agendamentos disponíveis."},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response({"appointments": appointments})
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AllRepairsView(APIView):
    def get(self, request):
        try:
            repairs = get_all_repairs()
            if not repairs:
                return Response(
                    {"message": "Não há reparações disponíveis."},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response({"repairs": repairs})
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AllUsersView(APIView):
    def get(self, request):
        try:
            users = get_all_users()
            if not users:
                return Response(
                    {"message": "Não há utilizadores disponíveis."},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response({"users": users})
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class UserAppointmentsView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'O parâmetro user_id é obrigatório'}, status=400)
        
        try:
            # Busca os agendamentos no DynamoDB
            appointments_data = get_appointments_by_user(user_id)
            
            # Formata a resposta
            formatted_appointments = []
            for app in appointments_data.get('appointments', []):
                formatted_appointments.append({
                    'date': app.get('appointment_date', ''),
                    'time_slot': app.get('time_slot', ''),
                    'service_type': app.get('service_type', ''),
                    'status': app.get('status', ''),
                    'request_id': app.get('request_id', ''),
                    'final_cost': app.get('final_cost', 0.0),
                    'technician_notes': app.get('technician_notes', ''),
                })
            
            return Response({
                "user_id": user_id,
                "appointments": formatted_appointments
            })
            
        except Exception as e:
            return Response({
                "error": str(e),
                "user_id": user_id,
                "appointments": []
            }, status=500)
        

