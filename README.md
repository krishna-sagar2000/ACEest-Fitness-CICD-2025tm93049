# ACEest Fitness and Gym - CI/CD Pipeline

A Flask web application for ACEest Fitness and Gym, built incrementally across versions 1.0 to 3.2.4, with a full CI/CD pipeline using Jenkins, Docker, and automated deployment to staging and production.

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


## Environment Variables
- `PORT` - port to run on (default 5000)
- `DEBUG` - enable debug mode (default false)
- `ADMIN_USERNAME` / `ADMIN_PASSWORD` - admin dashboard credentials

## Deployment
- Staging URL: TBD
- Production URL: TBD
