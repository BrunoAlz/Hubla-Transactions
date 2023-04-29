import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from core.models import User

class JWTAuthentucation:
    """
    Cria o Token JWT utilizando a Lib: https://pyjwt.readthedocs.io/en/stable/
    Authentica o usuário utilizando a função Authenticate
    """
    def authenticate(self, request):
        """
            Recebe o token na requisição do usuário se authentica, permite que ele
            acesse as views authenticadas.      
        """
        # Obter o token JWT da Requisição
        auth_header = get_authorization_header(request).decode('utf-8')
        if not auth_header or 'Bearer' not in auth_header:
            return None
        token = auth_header.split(' ')[1]

        # Tenta Decodificar o Token e extrair o id do usuário
        try:
            payload = jwt.decode(token, "CHAVE_SECRETA_LEMBRAR_DE_MUDAR", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expirado.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token inválido.')
        # Extrai o id do usuário
        user_id = payload['user_id']

        # Faz a query no banco para para tentar buscar o usuário
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Usuário não encontrado.')

        return (user, None)

    # Método para gerar o TOKEN 
    @staticmethod
    def generate_jwt(id):
        """
            Método para gerar o JWT https://pyjwt.readthedocs.io/en/stable/#example-usage
        """
        #Cria o Payload para montar o JTW
        payload = {
            # Passa o Id do Usuário
            'user_id': id,
            # Passa a Data de Expiração
            # “exp” (Expiration Time) Claim
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            # passa a outra data
            # “iat” (Issued At) Claim
            'iat': datetime.datetime.utcnow(),
        }

        # CRIAR A CHAVE SECRETA NO .env!!!!
        return jwt.encode(payload, "CHAVE_SECRETA_LEMBRAR_DE_MUDAR", algorithm="HS256")
        