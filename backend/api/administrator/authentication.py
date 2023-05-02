import jwt
import datetime
from rest_framework import exceptions
from rest_framework.authentication import  get_authorization_header
from core.models import User
from decouple import config

class JWTAuthentucation:
    """
    Provides authentication using JSON Web Tokens (JWT).

    This class generates and decodes JWT tokens using the PyJWT library
    (https://pyjwt.readthedocs.io/en/stable/).
    It also provides an `authenticate` method that extracts the token
    from the user's request, decodes it,
    and returns the user associated with the token if the
    authentication is successful.

    Methods:
        `authenticate(request):`
        Authenticates the user using the token provided in the request header.
        Returns the user associated with the token if the authentication is
        successful. Otherwise, raises an `AuthenticationFailed` exception.

        `generate_jwt(id):`
        Generates a new JWT token for the given user id. The token contains
        the user id, an expiration time, and an issued-at time. Returns the
        encoded JWT token as a string.
    """
    def authenticate(self, request):
        """
        Authenticates the user using the token provided in the request header.
        Returns the user associated with the token if the authentication is
        successful. Otherwise, raises an `AuthenticationFailed` exception.
        """
        # Get the token in the Request sent by the user
        auth_header = get_authorization_header(request).decode('utf-8')
        if not auth_header or 'Bearer' not in auth_header:
            return None
        token = auth_header.split(' ')[1]

        # Decode the Token and extract the user id
        try:
            payload = jwt.decode(token, f"{config('SECRET_KEY')}", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired token.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token.')
        
        # Extract the user id
        user_id = payload['user_id']

        # Query the database to try to find the user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found.')

        return (user, None)

    # Method to generate the TOKEN
    @staticmethod
    def generate_jwt(id):
        """
        Generates a new JWT token for the given user id.

        `Args:`
            id (int): The id of the user to associate with the token.

        `Returns:`
            str: The encoded JWT token as a string.
        """

        # Create the Payload to assemble the JTW
        payload = {
            # User Id
            'user_id': id,
            # “exp” (Expiration Time) Claim
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            # “iat” (Issued At) Claim
            'iat': datetime.datetime.utcnow(),
        }

        return jwt.encode(payload, f"{config('SECRET_KEY')}", algorithm="HS256")
