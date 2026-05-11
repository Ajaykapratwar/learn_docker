# Logistics Backend Architecture (Docker Demo)

An intermediate-level backend system demonstrating practical Docker and containerization skills, inspired by modern logistics and delivery platforms like Porter.

## Architecture

This project uses a multi-container architecture orchestrated by Docker Compose:
- **FastAPI (API)**: The main web server handling delivery requests.
- **PostgreSQL (DB)**: Relational database for persistent storage of deliveries.
- **Redis (Cache/Broker)**: Used for caching API visits and as a message broker for Celery.
- **Celery (Worker)**: Background worker process for asynchronous tasks (e.g., simulating driver dispatch).
- **Nginx (Proxy)**: Reverse proxy routing external traffic to the API.

## Containerization Concepts Showcased
- **Multi-container Orchestration**: `docker-compose.yml` ties 5 services together.
- **Dockerfiles**: Custom images for the Python backend and Nginx proxy.
- **Container Networking**: Services communicate over a custom bridge network (`backend_network`).
- **Volumes**: Persistent data storage for PostgreSQL (`postgres_data`).
- **Environment Variables**: Dynamic configuration passed via Compose to the application containers.
- **Healthchecks**: Ensures dependent services (db, redis) are ready before the API and worker start.

## Running Locally

1. Clone the repository.
2. Ensure Docker and Docker Compose are installed.
3. Run the following command at the root of the repository:
   ```bash
   docker-compose up --build -d
   ```
4. Access the API at `http://localhost`.
   - The interactive API documentation is available at `http://localhost/docs`.

## Usage
- Check API health and Redis caching: `GET http://localhost/`
- Create a delivery (triggers background task): 
  ```bash
  curl -X POST "http://localhost/deliveries/" -H "Content-Type: application/json" -d '{"item_name": "Laptop", "destination": "123 Main St"}'
  ```
- Check delivery status (should update from `pending` to `dispatched` after 5 seconds):
  ```bash
  curl -X GET "http://localhost/deliveries/1"
  ```
