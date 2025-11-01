import os
import json
from env_setup import EnvSetup
from nginx_setup import NginxSetup
from project_setup import ProjectSetup
from db_setup import DBSetup
from frontend_setup import FrontendSetup
from backend_setup import BackendSetup
from github_setup import GitHubSetup
from dev_env_setup import DevEnvSetup

def log(printable):
    print(' * ', end='')
    print(printable)

def main():
    # Read configuration from config.json
    CONFIG_PATH = "config.json"
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"{CONFIG_PATH} not found. Please create it or copy from config.json.template.")
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    steps = [
        "Project local setup",
        "Frontend setup",
        "Backend setup",
        "DB setup",
        "Nginx setup",
        "Env files setup",
        "GitHub setup",
        "Pipeline setup",
        "Dev environment setup"
    ]

    print("Kickstart My Project - Setup Steps")
    print("==================================")
    for idx, step in enumerate(steps, 1):
        print(f"{idx}. {step}")
    print("\nWhich step would you like to execute?")
    print("Enter the step number (e.g. 1), a comma-separated list (e.g. 1,3,5), a range (e.g. 2-6), or press Enter to execute all steps.")

    selection = input("Selection (or type 'cancel' to exit): ").strip()
    if selection.lower() == "cancel":
        print("Setup cancelled.")
        return
    if not selection:
        selected_steps = list(range(1, len(steps) + 1))
    else:
        selected_steps = []
        for part in selection.split(","):
            part = part.strip()
            if part.lower() == "cancel":
                print("Setup cancelled.")
                return
            if "-" in part:
                try:
                    start, end = map(int, part.split("-"))
                    if 1 <= start <= end <= len(steps):
                        selected_steps.extend(range(start, end + 1))
                    else:
                        print(f"Range {part} is out of range.")
                except ValueError:
                    print(f"Invalid range input: {part}")
            elif part.isdigit():
                num = int(part)
                if 1 <= num <= len(steps):
                    selected_steps.append(num)
                else:
                    print(f"Step number {num} is out of range.")
            else:
                print(f"Invalid input: {part}")

    # Remove duplicates and sort
    selected_steps = sorted(set(selected_steps))

    # Run selected steps
    for step_num in selected_steps:
        step_name = steps[step_num - 1]
        print(f"\nRunning step {step_num}: {step_name}")
        if step_num == 1:
            setup = ProjectSetup(config, log)
            setup.run()
        elif step_num == 2:
            frontend_setup = FrontendSetup(config, log)
            frontend_setup.run()
        elif step_num == 3:
            backend_setup = BackendSetup(config, log)
            backend_setup.run()
        elif step_num == 4:
            db_setup = DBSetup(config, log)
            db_setup.run()
        elif step_num == 5:
            nginx_setup = NginxSetup(config, log)
            nginx_setup.run()
        elif step_num == 6:
            env_setup = EnvSetup()
            env_setup.run()
        elif step_num == 7:
            github_setup = GitHubSetup(config, log)
            github_setup.run()
        elif step_num == 8:
            # Pipeline setup placeholder
            pass
        elif step_num == 9:
            dev_env_setup = DevEnvSetup(config, log)
            dev_env_setup.run()
        else:
            pass

if __name__ == "__main__":
    main()