# API Gateway

## Overview

This API Gateway serves as the entry point for the moderation service, handling requests and routing them to the appropriate backend services. It provides endpoints for health checks, moderation tasks, and metrics.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Moderation](#moderation)
  - [Metrics](#metrics)
- [Security Considerations](#security-considerations)
- [Testing](#testing)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/moderation_service.git
   cd moderation_service/api_gateway
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env.development` file:

   ```env
   # Redis URL for local development. If using the API Gateway as a Docker container
   # and want to access the local machine's Redis instance, use:
   # redis://host.docker.internal:6379
   REDIS_URL=redis://localhost:6379

   # Base URL for the moderation service
   MODERATION_SERVICE_BASE_URL=http://localhost:8001

   # Secret key for securing access to the moderation service
   GATEWAY_KEY=your_secret_key # default is 'secret'

   # Log level for the application. Default is 'INFO'.
   LOG_LEVEL= # default is INFO
   ```

## Usage

To run the API Gateway, use the following command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

### Health Check

- **GET** `/health`

  - Description: Checks the health of the API Gateway.
  - Response:
    - `200 OK`: Service is healthy.
    - `500 Internal Server Error`: Service is unhealthy.

- **GET** `/health/moderation-service`
  - Description: Checks the health of the moderation service.
  - Response:
    - `200 OK`: Moderation service is healthy.
    - `503 Service Unavailable`: Moderation service is down.

### Moderation

- **POST** `/moderate`

  - Description: Submits text for moderation.
  - Request Body:
    ```json
    {
      "text": "Sample text for moderation."
    }
    ```
  - Response:
    - `200 OK`: Task added successfully with a moderation ID.
    - `400 Bad Request`: Text cannot be empty.
    - `500 Internal Server Error`: An error occurred during moderation.

- **GET** `/result/{id}`
  - Description: Retrieves the result of a moderation task by ID.
  - Response:
    - `200 OK`: Returns the moderation result.
    - `404 Not Found`: Moderation result not found.
    - `500 Internal Server Error`: An error occurred during moderation.

### Metrics

- **GET** `/metrics`
  - Description: Exposes Prometheus metrics for monitoring.
  - Response:
    - `200 OK`: Returns metrics in plain text format.

## Security Considerations

- **Authentication**: Use the `GATEWAY_KEY` to secure access to the moderation service. Ensure that this key is kept secret and not exposed in public repositories.
- **Rate Limiting**: Implement rate limiting to prevent abuse of the moderation endpoints. The default is set to 10 calls per minute.
- **Input Validation**: Validate all incoming requests to ensure data integrity.

## Testing

To run the tests, navigate to the `api_gateway` directory and execute:

```bash
pytest tests/
```
