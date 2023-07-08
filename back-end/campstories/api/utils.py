import boto3
from django.core.files.base import ContentFile
import os
from twilio.rest import Client
from .models import StoryPictureRand
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication


def send_sms(phone_number, content):
    account_sid = "ACf3e5e6366e9bb9a563cb50b5ba9c0bf3"
    auth_token =  "283fe7fd6bd18a536f606b17f717c4b3"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=content,
        from_='+15812033514',
        to=phone_number
    )
    print(message)

def generate_audio(story):
    polly_client = boto3.client('polly')
    ssml = f"<speak><prosody rate='slow'>{story.content}</prosody></speak>"
    response = polly_client.synthesize_speech(TextType='ssml', Text=ssml, OutputFormat='mp3', VoiceId='Joanna')
    audio_stream = response['AudioStream'].read()
    
    # Create the ContentFile from the audio stream
    audio_file = ContentFile(audio_stream)

    # Save the audio file to the story instance
    story.audio_file.save(f'{story.id}.mp3', audio_file, save=True)

def generate_picture(story):
    random_picture = StoryPictureRand.objects.filter(genre=story.story_type).order_by('?').first()
    
    if random_picture is None : 
        random_picture = StoryPictureRand.objects.filter(id=41).first()
        
    print (random_picture)
    story.picture = random_picture

    story.save()


def AuthCheck (request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
    if authorization_header.startswith('Bearer '):
        token = authorization_header.split(' ', 1)
        token = token[1]
    try:
        # Manually authenticate the user using the token
        authentication = JWTAuthentication()
        validated_token = authentication.get_validated_token(token)
        user = authentication.get_user(validated_token)
        # Assign the authenticated user to request.user
        return user
    except:
        return None 