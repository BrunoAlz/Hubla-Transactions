from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from core.models import User
from core.serializers import UserSerializer
from rest_framework import status
from .authentication import JWTAuthentucation


class RegisterUserView(APIView):
    """
    This view allows the creation of users in the system.

    Methods:
        post(request):
        Receives user data in the request body and creates a new user
        with that data.
        Returns a success message and a 200 OK status code if the user
        is created successfully.
        Returns an error message and a 400 Bad Request status code if
          the user data is invalid.
    """

    def post(self, request):
        """
        Args:
            request (HttpRequest): The request object that contains
            the user data in the request body.

        Returns:
            Response:
            A response object that contains a success message
            and a 200 OK status code if the user is created,
            An error message and a 400 Bad Request status code
            if the user data is invalid.
        """
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "User registred!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    """
    This view allows users to log in to the system.

    Attributes:
        None

    Methods:
        post(request):
        Receives user data in the request body and authenticates
        the user using their email and password.

        Returns a success response containing the user data
        and a JWT token if the authentication is successful.

        Returns an error message and a 401 Unauthorized status
        code if the email or password is incorrect.
    """

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed(
                {'error': 'Please check your credentials!'})

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                {'error': 'Please check your credentials!'})

        token = JWTAuthentucation.generate_jwt(user.id)
        return Response([{'user': UserSerializer(user).data, 'token': token}], status=status.HTTP_200_OK)
