from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

CONFIG_STRING = """
SECRET_KEY=%s

DB_ENGINE='django.db.backends.mysql'
DB_NAME='hublatransactions'
DB_USERNAME='root'
DB_PASSWORD=''
DB_HOST='localhost'
DB_PORT=3306

""".strip() % get_random_string(50, chars)


# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)


CONFIG_EXAMPLE = """
SECRET_KEY=''

DB_ENGINE=''
DB_NAME=''
DB_USERNAME=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''

""".strip()

# Writing our configuration file to '.env-example'
with open('.env.example', 'w') as configfile:
    configfile.write(CONFIG_EXAMPLE)
