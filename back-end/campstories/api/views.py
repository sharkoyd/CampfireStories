from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404
import requests
import json


from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import PendingCode,UserProfile,Story

from django.contrib.auth.models import User

from rest_framework import status


import os,openai
from dotenv import load_dotenv


from rest_framework.permissions import IsAuthenticated
from .models import UserProfile

from django.core import serializers
from django.http import JsonResponse

from .serializers import StorySerializer
from django.db.models import F, Func

import random


import re

from . import utils

import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError


from django.core.files.base import ContentFile



load_dotenv()
api_key = os.getenv('OPENAI_KEY',None)
openai.api_key = api_key


@api_view(['GET'])
def Home(request):
    user = utils.AuthCheck(request)
    if user is None : 
        return JsonResponse({'message': 'You are not logged In'}, status=404)
    # Check if the user has associated profiles
    
    profile_id = request.query_params.get('profile_id')
    request.user = user
    # Get the user's profile
    # also performs as a  check for if the profile does not belong to the logged-in user
    profile = get_object_or_404(UserProfile, id=profile_id, user=user)



    # Get the age range for story filtering
    age_range_min = profile.age - 3
    age_range_max = profile.age + 3

    number_of_stories_to_fetch = 3


     # Get the highest score type
    highest_score_type = max(profile.get_scores(), key=profile.get_scores().get)

    # Fetch recommended stories from the database within the age range

    # Fetch random stories from the database within the age range
    recommended = Story.objects.filter(age_range__gte=age_range_min, age_range__lte=age_range_max, story_type=highest_score_type).order_by('?')[:number_of_stories_to_fetch]
    one_minute_stories = Story.objects.filter(age_range__gte=age_range_min, age_range__lte=age_range_max, length_minutes=1).order_by('?')[:number_of_stories_to_fetch]
    three_minute_stories = Story.objects.filter(age_range__gte=age_range_min, age_range__lte=age_range_max, length_minutes=3).order_by('?')[:number_of_stories_to_fetch]
    five_minute_stories = Story.objects.filter(age_range__gte=age_range_min, age_range__lte=age_range_max, length_minutes=5).order_by('?')[:number_of_stories_to_fetch]
    ten_minute_stories = Story.objects.filter(age_range__gte=age_range_min, age_range__lte=age_range_max, length_minutes=10).order_by('?')[:number_of_stories_to_fetch]

    # Serialize the stories 
    one_minute_serializer = StorySerializer(one_minute_stories, many=True)
    three_minute_serializer = StorySerializer(three_minute_stories, many=True)
    five_minute_serializer = StorySerializer(five_minute_stories, many=True)
    recommended_serializer = StorySerializer(recommended, many=True)
    print(recommended_serializer.data)
    print(one_minute_serializer.data)
    print(three_minute_serializer.data)
    print(five_minute_serializer.data)
    ten_minute_serializer = StorySerializer(ten_minute_stories, many=True)

    # Return the serialized stories
    phone_num = user.username.replace("."," ")
    full_name = user.first_name + " "+user.last_name
    return Response({
        'recommended': recommended_serializer.data,
        'one_minute_stories': one_minute_serializer.data,
        'three_minute_stories': three_minute_serializer.data,
        'five_minute_stories': five_minute_serializer.data,
        'full_name': full_name,
        'phone_number': phone_num,
        'password': user.password,
    })

#########
#important : there is the option to make the stories generated by this function visible to the public or not (the public can see them in the home screen recomandation)
#⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇⬇⬇⬇⬇⬇⬇⬇⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️
#in the admin pannel you can change the value of the field "validated" to True or False
#the stories generated by this function (from the openai api) are not very good and not well fitting to their time ranges and age ranges (api problem)
# and are NOT SAFE !!!
#to populate the database with better stories and more better fitting to their time ranges and age ranges use the admin pannel
#note: using the prompts i integrated in this function in the normal in CHAT GPT interface will generate [ far more better stories ] which will improve the quality of the app averall when added to the database manually

#contact the developer for more info and customization advice
#@b1chir on instagram
#https://www.linkedin.com/in/bechir-hamdi-1417aa264/

#this function and the utils.py file are the only files that use the aws polly api. configure your environment variables with your aws credentials to use it
# the aws polly api is used to generate audio files from the stories generated by the openai api
#follow these instructions to configure your aws credentials : https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html 

#AWS configuration settings are stored in plaintext files named credentials and config. These files use a simple format with sections called profiles. Each profile contains settings like access keys, regions, and output formats.

# The credentials file stores sensitive credential information. It includes profiles like [default] (use default) and [user1]. Each profile has settings for aws_access_key_id, aws_secret_access_key, and optionally aws_session_token.

# The config file stores other configuration settings. It includes profiles like [default] (use default) and [profile user1]. Each profile can have settings like region and output.

# By default, the files are located in the .aws folder in your home directory (on windows C:\Users\bechir\.aws). You can specify a different location using the AWS_CONFIG_FILE and AWS_SHARED_CREDENTIALS_FILE environment variables.

############


@api_view(['POST'])
def CustomStory(request):

    # Get the token from the query parameters
    user = utils.AuthCheck(request)
    if user is None : 
        return JsonResponse({'message': 'You are not logged In'}, status=404)

    request.user = user
    # Get the profile ID from the request
    profile_id = request.query_params.get('profile_id')

    # Get the user's profile
    profile = get_object_or_404(UserProfile, id=profile_id, user=user)
    print (profile.user)
    print (request.user)
    if profile.user != request.user:
        return Response({'message': 'Profile does not belong to the logged-in user'}, status=403)

    # Extract the necessary information from the request data
    involving = request.data.get('involving')
    age_range = request.data.get('age_range')
    duration = request.data.get('duration')
    if age_range =='0':
        age_range = profile.age


    #prompt customization
    print (duration)
    duration = str(int (duration) + 5) 
    if int(age_range) < 5:
        prompt = f"generate a very long easy {(duration)} minutes story that involves {involving} using repetitive phrases or rhymes,Basic vocabulary and simple sentence structures,Clear and straightforward plotlines, present it in a json format with the keys : title,content,gender(M,F,A(for any gender)),genre (oneword) from these action , adventure , comedy ,fantasy, mystery, science fiction,fairy tale , animal, educational or historical" 
    if int(age_range) >= 5 and int(age_range) < 8:
        prompt = f"generate a very long {duration} minutes story that involves {involving} using multiple characters, subplots Exploration of emotions, friendships, and problem-solving, present it in a json format with the keys : title,content,gender(M,F,A(for any gender)),genre (oneword) from these action , adventure , comedy ,fantasy, mystery, science fiction,fairy tale , animal, educational or historical" 
    if int(age_range) >= 8:
        prompt = f"generate a very long complex {duration} minutes story that involves {involving} using storylines and character development,Advanced vocabulary and language usage, present it in a json format with the keys : title,content,gender(M,F,A(for any gender)),genre (oneword) from these action , adventure , comedy ,fantasy, mystery, science fiction,fairy tale , animal, educational or historical" 

    
    response=openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        temperature= 0 ,
        max_tokens= 4000,
        top_p= 1,
        frequency_penalty= 0,
        presence_penalty= 0,
        stop= ["&"],
    
    )
    generated_text = response["choices"][0]["text"]

    # Remove \n characters
    generated_text = generated_text.replace('\n', '')

    # Convert to JSON format
    generated_text = json.loads(generated_text)

    # Add age_range field
    generated_text["age_range"] = age_range
    print (generated_text["genre"])
    try:
       

        # Create the Story object
        story = Story(
            title=generated_text['title'],
            content=generated_text['content'],
            age_range=generated_text['age_range'],
            gender=generated_text['gender'],
            story_type=generated_text['genre'].lower(),
            length_minutes=duration,
            validated=False
        )

        # Save the story object to generate an ID
        story.save()

        print("Story created successfully")

    except (BotoCoreError, NoCredentialsError) as e:
        # Handle any exceptions that may occur
        print("Error:", str(e))

    # Create the response data
    response_data = {
        'story': generated_text['content'],
        'title': generated_text['title'],
        'audio_file': story.audio_file.url  # Get the URL of the saved audio file
    }



    # Return the generated story as the response
    return Response(response_data)








@api_view(['GET'])

def Profiles(request):    
    user = utils.AuthCheck(request)
    if user is None : 
        return JsonResponse({'message': 'You are not logged In'}, status=404)
    # Check if the user has associated profiles
    profiles = UserProfile.objects.filter(user=user)
    if profiles.exists():
        # Serialize the profiles to JSON
        serialized_profiles = serializers.serialize('json', profiles)
        #print (serialized_profiles)
        print (profiles)
        profile_list = []
        for profile in profiles:
            profile_info = {
                'profile_id' :profile.id, 
                'name': profile.name,
                'profileimg': profile.profileimg,
            }
            profile_list.append(profile_info)
        print(profile_list)
        return JsonResponse({'profiles': profile_list}, status=200)
    else:
        return JsonResponse({'profiles': None}, status=200)

@api_view(['POST'])
def LoginWithPhoneNum(request):
    country_code = request.data.get('country_code')
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone_number or not password:
        return Response({'message': 'Invalid request data'}, status=400)

    username = f"{country_code}.{phone_number}"

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # User credentials are valid, set the pending code
         # Code is valid, generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        # Return the JWT tokens in the response
        return Response({
            'message': 'Valid',
            'refresh': str(refresh),
            'access': str(access_token),
        } , status=200)
        
    else:
        return Response({'message': 'Wrong Password or Phone number'}, status=401)




@api_view(['POST'])
def PhoneNumConfirm(request):
    country_code = request.data.get('country_code')
    phone_number = request.data.get('phone_number')

    username = f"{country_code}.{phone_number}"

    if User.objects.filter(username=username).exists():
        user=User.objects.get(username=username)
        if user.is_active : 
            return Response({'message': 'This number is already used'},status=400)

    else:
        user = User.objects.create_user(username=username, password='999999' ,is_active=False)
    
    try:
        pending_code = PendingCode.objects.get(user=user)
    except PendingCode.DoesNotExist:
        pending_code = PendingCode.objects.create(user=user)
    user.code.save()  # Save to generate new code
    pending_code.code = str(user.code)  # Set the code from user.code
    pending_code.save()  # Save the pending code
    phn=f"{country_code}{phone_number}"
    utils.send_sms(phn, f"Your code is {pending_code.code}")

    return Response({'message': 'Valid'},status=200)


@api_view(['POST'])
def VerifySignUpCode(request):
    code = request.data.get('verification_code')
    country_code = request.data.get('country_code')
    phone_number = request.data.get('phone_number')
    username = f"{country_code}.{phone_number}"
    print(username)
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    user=User.objects.get(username=username)

    if not code:
        print ("cccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
        return Response({'message': 'Invalid'}, status=400)

    try:
        pending_code = PendingCode.objects.get(code=code,user=user)
        user = pending_code.user
    except PendingCode.DoesNotExist:
        return Response({'message': 'you did not request a code'}, status=401)

    if code == pending_code.code:
        # Delete the pending code
        pending_code.delete()
        #call the save method to generate a new code
        user.code.save()
        # Return the JWT tokens in the response
        return Response({'message': 'Valid'}, status=200)
        
    else:
        return Response({'message': 'Invalid'}, status=401)
    

@api_view(['POST'])
def RegisterWithPhoneNum(request):

    phone_number = request.data.get('phone_number')
    country_code = request.data.get('country_code')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')


    username = f"{country_code}.{phone_number}"

    if User.objects.filter(username=username).exists():
        #update the user
        user = User.objects.get(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.save()

    return Response({'message': 'success'}, status=200)





@api_view(['POST'])
def CreateProfile(request):
    print (request.data)
    user = utils.AuthCheck(request)
    if user is None : 
        return JsonResponse({'message': 'You are not logged In'}, status=404)
    
    try:
        # Extract the necessary information from the request data
        
       
        name = request.data.get('name')
        age = request.data.get('age')
        profilepic = request.data.get('profilepic')
        
        interest = request.data.get('interests').lower()
        # Retrieve the UserProfile instance
        # Create a profile for the authenticated user
       
        user_profile = UserProfile(user=user, name=name, age=age, profileimg=profilepic)
        
        user_profile.save()
        
        # Access the scores field and convert it to a Python dictionary
        scores = json.loads(user_profile.scores)
        
        # Update a specific field in the scores dictionary
        print (scores)
        print (interest)
        scores[interest] += 1  # Update the 'action' field (example)
        print ("ccccccccccccccccccccccccccc")
        # Convert the updated scores dictionary back to JSON
        updated_scores = json.dumps(scores)

        # Set the updated scores value to the scores field of the UserProfile instance
        user_profile.scores = updated_scores

        # Save the UserProfile instance
        user_profile.save()
        

        # Return a success response
        return Response({'message': 'Profile created successfully'})
    except:
        return Response({'message': 'Invalid params'}, status=404)


    

@api_view(['GET'])
def GetUserInfo(request):
    user = utils.AuthCheck(request)
    if user is None : 
        return JsonResponse({'message': 'You are not logged In'}, status=404)

    try:
        user = request.user
        # Retrieve the UserProfile instance
        user_profile = get_object_or_404(UserProfile, user=user)

        # Return the UserProfile instance in the response
        return Response({
            'first_name': user_profile.name,
            'last_name': user_profile.profilepic,
            'username': user.username,
        })
    except:
        return Response({'message': 'Invalid params'}, status=401)

# @api_view(['POST'])
# def SendCodeResetPassword (request) : 
#     country_code = request.data.get('country_code')
#     phone_number = request.data.get('phone_number')
#     username = f"+{country_code}.{phone_number}"
#     user = User.objects.filter(username=username).exists()
#     if user is not None:
#         # User credentials are valid, set the pending code
#         try:
#             pending_code = PendingCode.objects.get(user=user)
#         except PendingCode.DoesNotExist:
#             pending_code = PendingCode.objects.create(user=user)
#         pending_code.code = str(user.code)  # Set the code from user.code
#         pending_code.save()  # Save the pending code

#         utils.send_sms(phone_number, f"Your code is {pending_code.code}")
#         print(pending_code.code)

#         return Response({'message': 'Valid'})
#     else:
#         return Response({'message': 'Invalid'}, status=401)


# @api_view(['PATCH'])
# def ResetPassword
