import os
import zipfile
import shutil

class BackendSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.log = log

    def extract_backend_zip(self):
        backend_zip_path = os.path.join("resources", "backend", "backend.zip")
        backend_extract_path = os.path.join(self.project_name)
        os.makedirs(backend_extract_path, exist_ok=True)
        with zipfile.ZipFile(backend_zip_path, 'r') as zip_ref:
            zip_ref.extractall(backend_extract_path)
        self.log(f"Extracted '{backend_zip_path}' to '{backend_extract_path}'.")
        
    def copy_application_properties(self):
        src = os.path.join("resources", "backend", "application.properties")
        dest_dir = os.path.join(self.project_name, "backend", "src", "main", "resources")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "application.properties")
        if os.path.exists(src):
            shutil.copyfile(src, dest)
            self.log(f"application.properties copied to '{dest}'.")
        else:
            self.log(f"Source application.properties not found at '{src}'.")

    def copy_dockerfile(self):
        src = os.path.join("resources", "backend", "Dockerfile")
        dest_dir = os.path.join(self.project_name, "backend")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "Dockerfile")
        if os.path.exists(src):
            shutil.copyfile(src, dest)
            self.log(f"Dockerfile copied to '{dest}'.")
        else:
            self.log(f"Source Dockerfile not found at '{src}'.")

    def run(self):
        self.extract_backend_zip()
        self.copy_application_properties()
        self.copy_dockerfile()