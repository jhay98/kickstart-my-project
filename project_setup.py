import os
import zipfile

class ProjectSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.docker_hub_repo = config.get("DOCKER_HUB_REPO")
        self.log = log

    def mkdir(self):
        self.log("Creating project directory...")
        if not os.path.exists(self.project_name):
            os.makedirs(self.project_name)
            self.log(f"Folder '{self.project_name}' created.")
        else:
            self.log(f"Folder '{self.project_name}' already exists.")

    def copy_gitignore(self):
        self.log("Copying .gitignore to project directory...")
        src = os.path.join("resources", ".gitignore")
        dest = os.path.join(self.project_name, ".gitignore")
        if os.path.exists(src):
            with open(src, "r") as f_src, open(dest, "w") as f_dest:
                f_dest.write(f_src.read())
            self.log(f".gitignore copied to '{dest}'.")
        else:
            self.log(f"Source .gitignore not found at '{src}'.")

    def copy_and_interpolate_docker_compose(self):
        self.log("Copying and interpolating docker-compose template...")
        template_path = os.path.join("resources", "docker-compose-template.txt")
        output_path = os.path.join(self.project_name, "docker-compose.yml")
        if not os.path.exists(template_path):
            self.log(f"Template not found at '{template_path}'.")
            return
        with open(template_path, "r") as template_file:
            template = template_file.read()
        docker_compose_content = (
            template
            .replace("{project-name}", self.project_name)
            .replace("{docker-hub-repo}", self.docker_hub_repo)
        )
        with open(output_path, "w") as output_file:
            output_file.write(docker_compose_content)
        self.log(f"docker-compose.yml created at '{output_path}'.")

    def create_empty_readme(self):
        self.log("Creating empty README.md in project directory...")
        readme_path = os.path.join(self.project_name, "README.md")
        with open(readme_path, "w") as f:
            f.write("# " + self.project_name + "\n")
        self.log(f"Empty README.md created at '{readme_path}'.")

    def run(self):
        self.mkdir()
        self.copy_gitignore()
        self.copy_and_interpolate_docker_compose()
        self.create_empty_readme()