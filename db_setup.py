import os
import psycopg2
from sshtunnel import SSHTunnelForwarder
from util import dash_to_underscore

class DBSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.log = log

    def confirm_servers_running(self):
        response = input("Make sure both local and remote DB servers running. Type 'go' when ready:").strip().lower()
        if response != 'go':
            self.log("Please start both DB servers before continuing.")
            return False
        self.log("Going")
        return True

    def create_remote_db(self):
        db_name = dash_to_underscore(self.project_name) + "_db"
        user = self.config.get("POSTGRES_USER")
        password = self.config.get("POSTGRES_PASSWORD")
        ssh_host = self.config.get("SSH_HOST")
        ssh_port = self.config.get("SSH_PORT", 22)
        ssh_user = self.config.get("SSH_USER")
        ssh_key = self.config.get("SSH_KEY")
        remote_bind_port = 5432

        self.log(f"Creating remote database '{db_name}' via SSH tunnel...")

        try:
            with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_pkey=ssh_key,
                remote_bind_address=('localhost', remote_bind_port)
            ) as tunnel:
                tunnel.start()
                conn = psycopg2.connect(
                    dbname="postgres",
                    user=user,
                    password=password,
                    host="127.0.0.1",
                    port=tunnel.local_bind_port
                )
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute(f"CREATE DATABASE {db_name};")
                self.log(f"Remote database '{db_name}' created.")
                cur.close()
                conn.close()
        except Exception as e:
            self.log(f"Error creating remote database: {e}")

    def run(self):
        if not self.confirm_servers_running():
            return
        self.create_remote_db()