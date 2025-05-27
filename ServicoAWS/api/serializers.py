import uuid
from rest_framework import serializers

class FaceRegisterSerializer(serializers.Serializer):
    image = serializers.ImageField()
    
    def create(self, validated_data):
        validated_data['user_id'] = str(uuid.uuid4())
        return validated_data

class FaceLoginSerializer(serializers.Serializer):
    image = serializers.ImageField()

class CardSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    expiration_month = serializers.CharField()
    expiration_year = serializers.CharField()
    cardholder_name = serializers.CharField()

class RepairRequestSerializer(serializers.Serializer):
    service_type = serializers.CharField()
    appointment_date = serializers.DateTimeField()
    time_slot = serializers.CharField()
    #card = CardSerializer()
    
class RepairStatusSerializer(serializers.Serializer):
    request_id = serializers.CharField()
    
class ClientApprovalSerializer(serializers.Serializer):
    request_id = serializers.UUIDField()
    aprovado = serializers.BooleanField()
    
class ConfirmarPresencaSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    request_id = serializers.CharField()
    presente = serializers.BooleanField()
    
class StaffConcluiReparacaoSerializer(serializers.Serializer):
    request_id = serializers.CharField()
    user_id = serializers.CharField()
    
class ConfirmarPagamentoSerializer(serializers.Serializer):
    request_id = serializers.CharField()

class ConfirmarRecolhaSerializer(serializers.Serializer):
    request_id = serializers.CharField()
    user_id = serializers.CharField()
