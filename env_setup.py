import os
import subprocess
from util import dash_to_underscore

class EnvSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.log = log

    def interpolate_template(self, template_path, dest_path, replacements):
        with open(template_path, "r") as template_file:
            content = template_file.read()
        for key, value in replacements.items():
            content = content.replace(key, value)
        with open(dest_path, "w") as dest_file:
            dest_file.write(content)
        self.log(f"Created '{dest_path}' from template '{template_path}'.")

    def create_backend_env(self):
        backend_folder = os.path.join(self.project_name, "backend")
        os.makedirs(backend_folder, exist_ok=True)
        # Create logs folder inside backend
        logs_folder = os.path.join(backend_folder, "logs")
        os.makedirs(logs_folder, exist_ok=True)
        self.log(f"Logs folder created at '{logs_folder}'.")
        env_prod_template_path = os.path.join("resources", "backend", ".env_prod_template")
        env_path = os.path.join(backend_folder, ".env")
        replacements = {
            "{project-name}": self.project_name,
            "{project-name-underscore}": dash_to_underscore(self.project_name),
            "{postgres-user}": self.config.get("POSTGRES_USER", ""),
            "{postgres-password}": self.config.get("POSTGRES_PASSWORD", "")
        }
        self.interpolate_template(env_prod_template_path, env_path, replacements)

    def create_frontend_env(self):
        frontend_folder = os.path.join(self.project_name, "frontend")
        os.makedirs(frontend_folder, exist_ok=True)
        env_path = os.path.join(frontend_folder, ".env")
        env_content = (
            f"REACT_APP_PROJECT_NAME={self.project_name}\n"
            f"REACT_APP_API_URL=http://{self.project_name}-backend:8080/api/\n"
        )
        with open(env_path, "w") as f:
            f.write(env_content)
        self.log(f"Frontend .env file created at '{env_path}'.")

    def copy_envs_to_server(self):
        ssh_host = self.config.get("SSH_HOST")
        ssh_port = self.config.get("SSH_PORT", 22)
        ssh_user = self.config.get("SSH_USER")
        ssh_key = self.config.get("SSH_KEY")
        remote_base = f"/home/{ssh_user}/{self.project_name}"

        # Ensure remote project folder exists
        mkdir_cmd = [
            "ssh",
            "-i", ssh_key,
            "-p", str(ssh_port),
            f"{ssh_user}@{ssh_host}",
            f"mkdir -p {remote_base}/backend {remote_base}/frontend"
        ]
        try:
            subprocess.run(mkdir_cmd, check=True)
            self.log(f"Ensured remote folders exist: {remote_base}/backend and {remote_base}/frontend")
        except subprocess.CalledProcessError as e:
            self.log(f"Error creating remote folders: {e}")
            return

        # Copy backend .env
        local_backend_env = os.path.join(self.project_name, "backend", ".env")
        remote_backend_env = f"{remote_base}/backend/.env"
        scp_backend_cmd = [
            "scp",
            "-i", ssh_key,
            "-P", str(ssh_port),
            local_backend_env,
            f"{ssh_user}@{ssh_host}:{remote_backend_env}"
        ]
        try:
            subprocess.run(scp_backend_cmd, check=True)
            self.log(f"Copied backend .env to {remote_backend_env} on server.")
        except subprocess.CalledProcessError as e:
            self.log(f"Error copying backend .env: {e}")

        # Copy frontend .env
        local_frontend_env = os.path.join(self.project_name, "frontend", ".env")
        remote_frontend_env = f"{remote_base}/frontend/.env"
        scp_frontend_cmd = [
            "scp",
            "-i", ssh_key,
            "-P", str(ssh_port),
            local_frontend_env,
            f"{ssh_user}@{ssh_host}:{remote_frontend_env}"
        ]
        try:
            subprocess.run(scp_frontend_cmd, check=True)
            self.log(f"Copied frontend .env to {remote_frontend_env} on server.")
        except subprocess.CalledProcessError as e:
            self.log(f"Error copying frontend .env: {e}")

    def run(self):
        self.log("Starting environment file setup...")
        self.create_backend_env()
        self.create_frontend_env()
        self.copy_envs_to_server()
        self.log("Environment file setup complete.")

