# Moderation Service

## Overview

The `Moderation Service` is a FastAPI-based application designed to provide automated content moderation capabilities. It leverages machine learning models to analyze and filter user-generated content, ensuring compliance with community guidelines and legal standards.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [System Design](#system-design)
- [Model Design](#model-design)
- [API Design](#api-design)
  - [Moderate Text Endpoint](#moderate-text-endpoint)
  - [Get Moderation Result Endpoint](#get-moderation-result-endpoint)
  - [Health Check Endpoint](#health-check-endpoint)
- [Caching](#caching)
- [Failover Mechanism](#failover-mechanism)
- [Testing](#testing)

## Installation

To install the moderation service, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Content-Moderation-System.git
   ```
2. Navigate to the project directory:
   ```bash
   cd moderation_service
   ```
3. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up environment variables in a `.env.development` file:

   ```env
   # Database connection URL for the main database
   DATABASE_URL=postgresql+asyncpg://username:password@host:port/database_name

   # Database connection URL for the synchronous database
   SYNC_DATABASE_URL=postgresql://username:password@host:port/database_name

   # OpenAI API key for accessing OpenAI services
   OPENAI_API_KEY=your openai key

   # Redis URL for local development. If using the API Gateway as a Docker container
   # and want to access the local machine's Redis instance, use:
   # redis://host.docker.internal:6379
   REDIS_URL=redis://localhost:6379

   # Domain for the API Gateway
   API_GATEWAY_DOMAIN=localhost:8000

   # Secret key for securing access to the moderation service
   GATEWAY_KEY= # default is secret

   # Log level for the application. Default is 'INFO'.
   LOG_LEVEL= # default is INFO

   TEXT_MODERATION_API=http://localhost:8003 # api domain responsible for text moderation
   ```

## Usage

To start the moderation service, run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

You can then send requests to the API as described in the API Design section.

## System Design

The Moderation Service is a microservice designed to process text content asynchronously while ensuring high resilience and fault tolerance. Its key workflow is as follows:

### API Endpoint (/moderate/text)

- The service exposes a `/moderate` route that accepts a JSON payload containing a text field.
- Upon receiving a request, the service generates a unique `moderation_id` and immediately returns this ID to the client. This allows the client to later query the moderation result using the provided identifier.

### Asynchronous Task Processing

- The payload (including the text and the generated `moderation_id`) is pushed to a Celery task queue.
- Celery is integrated with RabbitMQ as its message broker. The RabbitMQ setup includes a dedicated Dead Letter Queue (DLQ) to capture tasks that exceed their retry limits or encounter non-recoverable errors.
- The task configuration features automatic retries with exponential backoff, ensuring robust handling of transient failures.

### Moderation and Data Persistence

- Once picked up by a Celery worker, the task calls the internal `ModerationService` to process the text. This may involve invoking external moderation APIs or applying internal logic.
- The resulting moderation decision (e.g., whether the content is flagged) is stored synchronously in a PostgreSQL database.
- Synchronous database operations are employed to ensure data consistency and simplicity in the persistence layer.

### Resilience and Fault Tolerance

- The use of RabbitMQ with a DLQ allows for proper handling of failed tasks. If a task repeatedly fails even after retries, it is routed to the DLQ for further analysis or manual intervention.
- This architecture decouples the immediate response from the heavier processing, ensuring that clients receive prompt feedback while processing continues asynchronously.

### Flow Diagram

![Flow Diagram](../screenshots/moderate_text_flow_diagram.png){: width="300" height="600"}

## Model Design

The moderation service utilizes several models defined in SQLAlchemy, including:

### ModerationResult Model

Represents the result of moderation actions.

#### Attributes

- `uuid`: Unique identifier for the moderation result (Primary Key, indexed).
- `text`: The content that is being moderated.
- `result`: A boolean indicating whether the content passed moderation.
- `meta`: The response got from OpenAI is stored for future needs.
- `created_at`: Timestamp of when the moderation action was created.
- `updated_at`: Timestamp of when the moderation action was last updated.

## API Design

The API provides endpoints for interacting with the moderation service. Below are the key endpoints:

### Moderate Text Endpoint

- **Endpoint**: `POST /v1/moderate/text`
- **Description**: Submits text for moderation.
- **Request Body**:
  ```json
  {
    "text": "string"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Task added",
      "moderation_id": "string"
    }
  }
  ```
- **Status Codes**:
  - `200 OK`: Moderation task successfully created.
  - `400 Bad Request`: Invalid input data.
  - `500 Internal Server Error`: An error occurred while processing the request.

### Get Moderation Result Endpoint

- **Endpoint**: `GET /v1/moderation/{id}`
- **Description**: Retrieves moderation results by ID.
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "moderation_result": true,
      "message": "Fetched result successfully!"
    }
  }
  ```
- **Status Codes**:
  - `200 OK`: Successfully fetched moderation result.
  - `404 Not Found`: Moderation result not found.
  - `500 Internal Server Error`: An error occurred while processing the request.

### Health Check Endpoint

- **Endpoint**: `GET /v1/health`
- **Description**: Checks the health status of the moderation service.
- **Response**:
  ```json
  {
    "success": true,
    "data": {
      "message": "Service is healthy"
    }
  }
  ```
- **Status Codes**:
  - `200 OK`: Service is running.
  - `500 Internal Server Error`: Service is down.

## Caching

The moderation service implements caching for the `/v1/moderation/{id}` endpoint using Redis. When a moderation result is requested, the service first checks the Redis cache to see if the result is already available. If it is, the cached result is returned, reducing the need for database queries and improving response times.

### Caching Workflow

1. **Check Cache**: When a request is made to retrieve moderation results, the service checks Redis for the result using the moderation ID.
2. **Return Cached Result**: If the result is found in the cache, it is returned immediately.
3. **Fetch from Database**: If the result is not found in the cache, the service queries the database for the moderation result.
4. **Store in Cache**: Once the result is retrieved from the database, it is stored in Redis for future requests.

This caching mechanism enhances performance and reduces the load on the database, allowing for faster response times for frequently requested moderation results.

## Failover Mechanism

### Redis Caching Failover

The caching mechanism in `redis.py` includes a failover strategy that ensures the application can gracefully handle Redis connection issues. If a Redis operation fails due to a timeout or connection error, the service logs the error and returns `None` instead of crashing. This allows the moderation service to continue functioning, albeit without caching, until Redis is available again.

### Celery Task Failover

In `moderation_tasks.py`, the Celery task for moderating text includes a robust failover mechanism. If an error occurs during the moderation process, the task will automatically retry up to three times with exponential backoff. If the task fails after the maximum number of retries, it is logged, and the task is moved to a Dead Letter Queue (DLQ) for further analysis. This ensures that transient errors do not disrupt the moderation process and allows for manual intervention if necessary.

## Testing

To run the tests, navigate to the `moderation_service` directory and execute:

```bash
pytest tests/
```
