import jwt, datetime

class JWTAuthentucation:
    """
    Criando o JWT utilizando a Lib: https://pyjwt.readthedocs.io/en/stable/
    """
    # Método para gerar o TOKEN 
    @staticmethod
    def generate_jwt(id):
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
        