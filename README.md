# Kickstart My Project

Bootstraps a skeleton for a lightweight web development project with:
- PostgreSQL database
- Spring Boot backend
- React frontend
- GitHub repository setup
- Docker Compose for orchestration
- Automated setup on EC2 instance
- CI/CD pipeline with GitHub Actions

## Prerequisites

Install the following dependencies before running the setup:

- Python 3.10+
- [gh (GitHub CLI)](https://cli.github.com/)
- [Node.js & npm](https://nodejs.org/) (for React frontend)
- Docker & Docker Compose
- AWS CLI (for EC2 setup)
- `psycopg2` Python package (`pip install psycopg2`)
- `sshtunnel` Python package (`pip install sshtunnel`)

## Setup Instructions

1. **Clone this repository** and enter the project directory.

2. **Configure your project:**
   - Copy `config.json.template` to `config.json` and fill in your values.

3. **Run the setup script:**
   ```sh
   python main.py
   ```
   - Follow the prompts to select which steps to run.

## Notes

- Make sure your AWS EC2 instance is set up with the required folder structure and installations.
- Sensitive files like `.env` and `application.properties` are ignored by Git and Docker.
- The pipeline will handle Docker Hub pushes automatically.
- Set the correct URLs and container names in your configuration.

## Project Structure

- `backend/` - Spring Boot backend
- `frontend/` - React frontend
- `db/` - Database configuration
- `logs/` - Log files
- `docker-compose.yml` - Docker orchestration
- `.gitignore` - Ignore sensitive/config files

## Pipeline

- CI/CD is set up via GitHub Actions for automated builds and deployments.