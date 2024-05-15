import boto3
from botocore.exceptions import ClientError
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_credentials():
    secret_arn = "arn:aws:secretsmanager:ap-south-1:982695942133:secret:rds!db-d8a0052a-7b38-4a80-a880-871f8553780d-yp2K4n"
    region_name = "ap-south-1"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response["SecretString"]
    
    try:
        credentials = json.loads(secret)
    except json.JSONDecodeError as e:
        print(f'Invalid json: {e}') 
    
    return credentials


credentials = get_db_credentials()

DB_HOST = "database-1.clmy8q0wsvlp.ap-south-1.rds.amazonaws.com"
DB_PORT = 5432
DB_NAME = "database-1"

# dialect+driver://username:password@host:port/database
DATABASE_URL = f"postgresql+psycopg2://{credentials['username']}:{credentials['password']}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)

session = SessionLocal()


print(session)