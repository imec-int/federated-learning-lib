from dotenv import load_dotenv
import dotenv
import psycopg2

# TODO place at entry point of application
load_dotenv()

envPath = "./examples/PHR/.env"

def connectToDb(database:str):
    dbUser = dotenv.get_key(envPath, "DB_USER")
    dbPw = dotenv.get_key(envPath, "DB_PASSWORD")
    dbHost = dotenv.get_key(envPath, "DB_HOST")
    dbPort = dotenv.get_key(envPath, "DB_PORT")
    return psycopg2.connect(database=database, user=dbUser, password=dbPw, host=dbHost, port=dbPort, sslmode='require')

hosp1Db = connectToDb("hospital1")
cur = hosp1Db.cursor()
cur.execute('SELECT gender, COUNT(*) FROM eicu_crd.patient GROUP BY gender')
rows = cur.fetchall()
for row in rows:
    print(row[0]+":\t"+str(row[1]))
hosp1Db.close()