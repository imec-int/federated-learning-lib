from dotenv import load_dotenv
import dotenv
import psycopg2

# TODO place at entry point of application
load_dotenv()

envPath = "./phr/.env"

class ScriptApi:

    def __init__(self) -> None:
        self.connection = None

    def get_postgresql_connection(self):
        if self.connection == None:
            dbUser = dotenv.get_key(envPath, "DB_USER")
            dbPw = dotenv.get_key(envPath, "DB_PASSWORD")
            dbHost = dotenv.get_key(envPath, "DB_HOST")
            dbPort = dotenv.get_key(envPath, "DB_PORT")
            dbName = dotenv.get_key(envPath, "DB_NAME")
            self.connection = psycopg2.connect(database=dbName, user=dbUser, password=dbPw, host=dbHost, port=dbPort, sslmode='require')
        return self.connection