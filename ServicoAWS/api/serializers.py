import uuid
from rest_framework import serializers

class FaceRegisterSerializer(serializers.Serializer):
    image = serializers.ImageField()
    
    def create(self, validated_data):
        validated_data['user_id'] = str(uuid.uuid4())
        return validated_data

class FaceLoginSerializer(serializers.Serializer):
    image = serializers.ImageField()
