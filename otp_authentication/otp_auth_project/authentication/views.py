from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .utils import generate_otp, verify_otp, send_otp_email
import jwt
from datetime import datetime, timedelta
import requests
from django.http import JsonResponse
@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')

    if not email:
        return JsonResponse({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)



    # Check if the user already exists
    if UserProfile.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = UserProfile(email=email)
    user.save()

    return JsonResponse({"message": "Registration successful. Please verify your email."}, status=status.HTTP_200_OK)

@api_view(['POST'])
    

def request_otp(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(UserProfile, email=email)

    otp_secret, otp_code = generate_otp(email)
    user.otp_hash = otp_secret
    user.save()

    send_otp_email(email, otp_code)

    return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp_entered = request.data.get('otp')

    if not email or not otp_entered:
        return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(UserProfile, email=email)

    if verify_otp(user.otp_hash, otp_entered):
        # Generate JWT token for session management
        token = generate_jwt_token(email)
        return Response({"message": "Login successful.", "token": token}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

def generate_jwt_token(email):
    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(hours=1)}, 'secret', algorithm='HS256')
    return token.decode('utf-8')



# Get CSRF token
response = requests.get('http://localhost:8000/api/get_csrf/')
csrf_token = response.cookies['csrftoken']

# Make POST request with CSRF token
headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token,
}
data = {
    'email': 'user@example.com',
}
response = requests.post('http://localhost:8000/api/register/', headers=headers, json=data)
print(response.json())
