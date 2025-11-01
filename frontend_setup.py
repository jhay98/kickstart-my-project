import os
import shutil
import subprocess

class FrontendSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.log = log

    def create_react_app(self):
        frontend_folder = os.path.join(self.project_name, "frontend")
        if not os.path.exists(frontend_folder):
            self.log(f"Creating React app in '{frontend_folder}'...")
            try:
                subprocess.run(
                    ["npx", "create-react-app", frontend_folder],
                    check=True
                )
                self.log("React app created successfully.")
            except subprocess.CalledProcessError as e:
                self.log(f"Error creating React app: {e}")
        else:
            self.log(f"Frontend folder '{frontend_folder}' already exists.")

    def copy_dockerfile(self):
        src = os.path.join("resources", "frontend", "Dockerfile")
        dest_dir = os.path.join(self.project_name, "frontend")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "Dockerfile")
        if os.path.exists(src):
            shutil.copyfile(src, dest)
            self.log(f"Dockerfile copied to '{dest}'.")
        else:
            self.log(f"Source Dockerfile not found at '{src}'.")

    def copy_dockerignore(self):
        src = os.path.join("resources", "frontend", ".dockerignore")
        dest_dir = os.path.join(self.project_name, "frontend")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, ".dockerignore")
        if os.path.exists(src):
            shutil.copyfile(src, dest)
            self.log(f".dockerignore copied to '{dest}'.")
        else:
            self.log(f"Source .dockerignore not found at '{src}'.")

    def run(self):
        self.create_react_app()
        self.copy_dockerfile()
        self.copy_dockerignore()