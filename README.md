# Chess Tournament Backend

This is a Django-based backend system for managing chess tournaments. It provides functionality for user management, tournament creation, match management, and result tracking.

## Features

- User authentication and authorization
- Tournament management
- Match creation and result recording
- Automated pairing generation
- Tournament standings calculation
- API documentation with Swagger

## Technologies Used

- Django 4.2+
- Django REST Framework
- Djoser for authentication
- Celery for asynchronous tasks
- PostgreSQL as the database
- Redis for caching and as a message broker
- Docker and Docker Compose for containerization

## Prerequisites

- Docker and Docker Compose

## Setup and Installation

1. Clone the repository:

`git clone https://github.com/ulugkhujayev/chess_tournament_backend.git`
`cd chess_tournament_backend`

2. Create a `.env` file in the project root and add the necessary environment variables:

`SECRET_KEY=secret_key`
`DEBUG=True`
`ALLOWED_HOSTS=localhost,127.0.0.1`
`DB_NAME=db_name`
`DB_USER=db_name`
`DB_PASSWORD=db_pass`
`DB_HOST=db`
`DB_PORT=5432`
`CELERY_BROKER_URL=redis://redis:6379/0`
`CELERY_RESULT_BACKEND=redis://redis:6379/0`

3. Build and run the Docker containers:
   `docker-compose up --build`


4. Create a superuser:
   `docker-compose exec web python manage.py createsuperuser`

## Usage

1. Access the API at `http://localhost:8000/api/`
2. View the API documentation at `http://localhost:8000/swagger/`
3. Use the `/auth/` endpoints for user registration and authentication
4. Use the `/api/tournaments/` endpoints to manage tournaments
5. Use the `/api/matches/` endpoints to manage matches

## Running Tests

To run the test suite:
`docker-compose exec web python manage.py test`

## API Endpoints

- `/api/users/`: User management
- `/api/tournaments/`: Tournament management
- `/api/matches/`: Match management
- `/auth/`: Authentication endpoints (provided by Djoser)

For detailed API documentation, visit the Swagger UI at `/swagger/`.
