import os
import re
import subprocess

class NginxSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.log = log

    def get_nginx_conf_from_ec2(self):
        ssh_host = self.config.get("SSH_HOST")
        ssh_port = self.config.get("SSH_PORT", 22)
        ssh_user = self.config.get("SSH_USER")
        ssh_key = self.config.get("SSH_KEY")
        conf_path = "/home/deploy-user/nginx/nginx.conf"

        self.log(f"Connecting to EC2 {ssh_user}@{ssh_host}:{ssh_port} to fetch Nginx config file '{conf_path}'...")

        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-p", str(ssh_port),
            f"{ssh_user}@{ssh_host}",
            f"cat {conf_path}"
        ]
        try:
            result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
            self.log("Fetched Nginx config successfully.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.log(f"Error fetching Nginx config: {e}")
            return None

    def edit_nginx_conf_on_ec2(self, new_content):
        ssh_host = self.config.get("SSH_HOST")
        ssh_port = self.config.get("SSH_PORT", 22)
        ssh_user = self.config.get("SSH_USER")
        ssh_key = self.config.get("SSH_KEY")
        conf_path = "/home/deploy-user/nginx/nginx.conf"

        self.log(f"Connecting to EC2 {ssh_user}@{ssh_host}:{ssh_port} to update Nginx config file '{conf_path}'...")

        # Use echo and ssh to overwrite the file with new_content
        # Safer to use a temporary file and then move it on the remote host
        try:
            # Write new_content to a temporary local file
            tmp_local = "nginx.conf.tmp"
            with open(tmp_local, "w") as f:
                f.write(new_content)

            # Copy the file to the remote host
            scp_cmd = [
                "scp",
                "-i", ssh_key,
                "-P", str(ssh_port),
                tmp_local,
                f"{ssh_user}@{ssh_host}:{conf_path}.tmp"
            ]
            subprocess.run(scp_cmd, check=True)
            self.log("Temporary config file copied to EC2.")

            # Move the temp file to the actual config file on the remote host
            ssh_cmd = [
                "ssh",
                "-i", ssh_key,
                "-p", str(ssh_port),
                f"{ssh_user}@{ssh_host}",
                f"mv {conf_path}.tmp {conf_path}"
            ]
            subprocess.run(ssh_cmd, check=True)
            self.log("Nginx config file updated on EC2.")

            # Remove the temporary local file
            os.remove(tmp_local)
        except Exception as e:
            self.log(f"Error updating Nginx config: {e}")

    def reload_nginx_on_ec2(self):
        ssh_host = self.config.get("SSH_HOST")
        ssh_port = self.config.get("SSH_PORT", 22)
        ssh_user = self.config.get("SSH_USER")
        ssh_key = self.config.get("SSH_KEY")
        container_name = self.config.get("NGINX_CONTAINER_NAME", "nginx-proxy")

        self.log(f"Reloading Nginx in container '{container_name}' on EC2 {ssh_user}@{ssh_host}:{ssh_port}...")

        ssh_cmd = [
            "ssh",
            "-i", ssh_key,
            "-p", str(ssh_port),
            f"{ssh_user}@{ssh_host}",
            f"docker exec {container_name} nginx -s reload"
        ]
        try:
            subprocess.run(ssh_cmd, check=True)
            self.log("Nginx reloaded successfully in container.")
        except subprocess.CalledProcessError as e:
            self.log(f"Error reloading Nginx: {e}")
    
    def add_routes(self, nginx_conf):
        placeholder = '# <---INSERT--->'
        template_path = os.path.join("resources", "nginx-conf-template.txt")
        with open(template_path, "r") as template_file:
            template = template_file.read()
        return nginx_conf.replace(placeholder, f'{template.replace('{project-name}', self.project_name)}\n\n  {placeholder}')


    def run(self):
        nginx_conf_content = self.get_nginx_conf_from_ec2()
        self.edit_nginx_conf_on_ec2(self.add_routes(nginx_conf_content))
        self.reload_nginx_on_ec2()
