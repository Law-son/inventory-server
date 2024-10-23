from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
@authentication_classes([])  # No authentication required for signup
@permission_classes([AllowAny])  # Allow all users to access this view
def signup(request):
    """
    Create a new user account using the provided details.
    """
    serializer = UserSerializer(data=request.data)
    
    # Validate the incoming data
    if serializer.is_valid():
        user = serializer.save()  # User is created here; password is already hashed
        token = Token.objects.create(user=user)  # Create token for the new user
        
        # Return success response with token
        return Response(
            {
                'status': 'success',
                'message': 'User account created successfully',
                'token': token.key
            },
            status=status.HTTP_201_CREATED
        )
    
    # Return error response with validation errors
    return Response(
        {
            'status': 'error',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@authentication_classes([])  # No authentication required for login
@permission_classes([AllowAny])  # Allow all users to access this view
def login(request):
    """
    Authenticate a user and return a token if successful.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    # Authenticate the user using email as username
    user = authenticate(username=email, password=password)

    if user is not None:
        # User is authenticated; check if token exists or create a new one
        token, created = Token.objects.get_or_create(user=user)
        
        # Serialize user data excluding password
        serializer = UserSerializer(user)

        # Return success response with token and user data
        return Response(
            {
                'status': 'success',
                'message': 'Login successful',
                'token': token.key,
                'user': serializer.data  # Include user data in the response
            },
            status=status.HTTP_200_OK
        )
    else:
        # Return error response for invalid credentials
        return Response(
            {
                'status': 'error',
                'message': 'Invalid email or password'
            },
            status=status.HTTP_401_UNAUTHORIZED
        )


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    print(f"Request Headers: {request.headers}")  # Debugging output
    print(f"Authenticated User: {request.user}")  # Check authenticated user

    try:
        # Get the token from the request
        token = request.auth  # `request.auth` contains the token for authenticated users
        
        # print(f"Token: {token}")  # Debugging output for the token
        
        # Delete the token
        if token:
            token.delete()  # Remove the token from the database
        
        return Response(
            {
                'status': 'success',
                'message': 'Logged out successfully'
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        # Handle the exception and return a suitable error response
        return Response(
            {
                'status': 'error',
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )