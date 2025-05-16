import boto3
from django.conf import settings


rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    aws_session_token=settings.AWS_SESSION_TOKEN,  # <-- aqui o token temporário
    region_name=settings.AWS_REGION
)

def add_face(user_id, image_bytes, collection_id='primeTechUsers'):
    response = rekognition.index_faces(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes},
        ExternalImageId=user_id,
        DetectionAttributes=['DEFAULT']
    )
    faces = response.get('FaceRecords', [])
    return faces[0]['Face']['FaceId'] if faces else None

def search_face(image_bytes, collection_id='primeTechUsers'):
    response = rekognition.search_faces_by_image(
        CollectionId=collection_id,
        Image={'Bytes': image_bytes},
        MaxFaces=1,
        FaceMatchThreshold=90
    )
    matches = response.get('FaceMatches', [])
    return matches[0]['Face']['FaceId'] if matches else None
