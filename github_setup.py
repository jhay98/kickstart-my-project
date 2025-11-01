import os
import subprocess

class GitHubSetup:
    def __init__(self, config, log=print):
        self.config = config
        self.project_name = config.get("PROJECT_NAME")
        self.token = config.get("GH_TOKEN")
        self.log = log

    def authenticate(self):
        if not self.token:
            self.log("GH_TOKEN not found in config. Please add your GitHub token.")
            return False
        self.log("Authenticating with GitHub using token...")
        try:
            subprocess.run(
                ["gh", "auth", "login", "--with-token"],
                input=self.token.encode(),
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"GitHub authentication failed: {e}")
            return False

    def create_github_repo(self):
        repo_name = self.project_name
        repo_path = os.path.join(os.getcwd(), repo_name)
        self.log(f"Creating GitHub repository '{repo_name}'...")

        # Initialize git repo if not present
        if not os.path.exists(os.path.join(repo_path, ".git")):
            subprocess.run(["git", "-C", repo_path, "init"], check=True)
            subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
            subprocess.run(["git", "-C", repo_path, "commit", "-m", "Initial commit"], check=True)

        try:
            subprocess.run(
                ["gh", "repo", "create", repo_name, "--private", "--source", repo_path, "--remote=origin", "--push"],
                check=True
            )
            self.log(f"GitHub repository '{repo_name}' created and initial files pushed.")
        except subprocess.CalledProcessError as e:
            self.log(f"Error creating GitHub repository: {e}")

    def run(self):
        if self.authenticate():
            self.create_github_repo()
