import jwt, datetime

class JWTAuthentucation:
    """
    Criando o JWT utilizando a Lib: https://pyjwt.readthedocs.io/en/stable/
    """
    def generate_jwt(self, id):
        #Cria o Payload para montar o JTW
        payload = {
            # Passa o Id do Usuário
            'user_id': id,
            # Passa a Data de Expiração
            'expire_time': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            # passa a outra data
            'date': datetime.datetime.utcnow(),
        }

        # CRIAR A CHAVE SECRETA NO .env!!!!
        return jwt.encode(payload, "CHAVE_SECRETA_LEMBRAR_DE_MUDAR", algorithm="HS256")
        