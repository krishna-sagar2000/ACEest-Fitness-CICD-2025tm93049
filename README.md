# ACEest Fitness and Gym - CI/CD Pipeline

A Flask web application for ACEest Fitness and Gym, built incrementally across versions 1.0 to 3.2.4, with a containerized build validated by both a Jenkins BUILD pipeline and an automated GitHub Actions CI pipeline.

## Features
- Program selection (Fat Loss, Muscle Gain, Beginner) with workout charts and diet plans
- Member signup with input validation
- Trainer session booking
- Logging of application activity
- Custom error handling (404/500)
- Analytics dashboard
- Protected admin dashboard (basic auth)
- Membership fee payment tracking

## Version History
- v1.0: Program selector baseline
- v1.1: Member signup form
- v1.1.2: Signup input validation
- v2.0.1: Trainer session booking
- v2.1.2: Logging
- v2.2.1: Custom error pages
- v2.2.4: Analytics route
- v3.0.1: Protected admin dashboard
- v3.1.2: Membership fee tracking
- v3.2.4: Final polish (environment config)

## Running locally

pip3 install -r requirements.txt
python3 app.py


The app runs on `http://localhost:5000` by default.

## Running tests manually

pip3 install -r requirements.txt
pytest


## Running with Docker

docker build -t aceest-fitness:latest .
docker run -d -p 5000:5000 --name aceest-fitness aceest-fitness:latest


The containerized app is then available at `http://localhost:5000`, identical in behaviour to running `app.py` directly.

## Environment Variables
- `PORT` - port to run on (default 5000)
- `DEBUG` - enable debug mode (default false)
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` - admin dashboard credentials

## CI/CD Pipeline Overview

This project is validated by two independent, automated pipelines:

### GitHub Actions (`.github/workflows/main.yml`)
Triggered automatically on every `push` and `pull_request`, on any branch. Runs three sequential jobs, each gated on the previous one succeeding:
1. **Build & Lint** - installs dependencies, compiles `app.py` to catch syntax errors, and lints the codebase with `flake8`.
2. **Docker Image Assembly** - builds the Docker image and saves it as a build artifact so the exact same image is reused in the next job.
3. **Automated Testing** - loads that image and runs the full `pytest` suite *inside the container*, confirming the containerized app behaves correctly, not just the raw source.

### Jenkins
A Jenkins Freestyle job (`ACEest-Build`) polls this repository and, on detecting a new commit on `main`:
1. Checks out the latest code from GitHub.
2. Installs dependencies and runs the `pytest` suite directly on the build server.
3. Builds the Docker image (`aceest-fitness:latest`), serving as a secondary, independent build gate before the image is considered ready.

### Why both
GitHub Actions gives fast, cloud-hosted feedback on every branch and pull request, while Jenkins provides a self-hosted build gate consistent with a traditional enterprise CI setup. Together they demonstrate that the same codebase builds, lints, and passes its full test suite - inside its container - across two independent automation tools.
