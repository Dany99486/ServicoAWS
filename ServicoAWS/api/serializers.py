import uuid
from rest_framework import serializers

class FaceRegisterSerializer(serializers.Serializer):
    image = serializers.ImageField()
    
    def create(self, validated_data):
        validated_data['user_id'] = str(uuid.uuid4())
        return validated_data

class FaceLoginSerializer(serializers.Serializer):
    image = serializers.ImageField()

class RepairRequestSerializer(serializers.Serializer):
    service_type = serializers.CharField()
    appointment_date = serializers.DateTimeField()
    
class RepairStatusSerializer(serializers.Serializer):
    request_id = serializers.CharField()
