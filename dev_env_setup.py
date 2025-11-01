import psycopg2
from util import dash_to_underscore


class DevEnvSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.log = log
    
    def create_local_db(self):
        db_name = dash_to_underscore(self.project_name) + "_db"
        user = self.config.get("POSTGRES_USER")
        password = self.config.get("POSTGRES_PASSWORD")
        host = "localhost"
        port = 5432
        self.log(f"Creating local database '{db_name}'...")

        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {db_name};")
            self.log(f"Local database '{db_name}' created.")
            cur.close()
            conn.close()
        except Exception as e:
            self.log(f"Error creating local database: {e}")

    def run(self):
        self.create_local_db()