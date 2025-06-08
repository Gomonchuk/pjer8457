hostname = "127.0.0.1"
username = "postgres"
password =  "jrAsWQ71R67"
port = "5432"
db_name = "app"

SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{hostname}:{port}/{db_name}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

