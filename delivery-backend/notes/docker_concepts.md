# Docker Concepts Applied

## 1. Multi-Stage / Custom Builds
We separate the `nginx` reverse proxy and the `backend` logic into their own directories, each with its own `Dockerfile`. The `api` and `worker` services share the same Python Dockerfile but run different commands (one runs `uvicorn`, the other `celery`), demonstrating image reusability.

## 2. Docker Networking
We define a custom bridge network `backend_network`. This allows containers to resolve each other by container name (e.g., the API connects to `db` using `postgresql://user:password@db:5432/...`).

## 3. Persistent Volumes
The PostgreSQL database uses a named volume `postgres_data`. If the database container is destroyed and recreated, the data persists on the host machine.

## 4. Healthchecks & Dependencies
In the `docker-compose.yml`, we use `depends_on` combined with `condition: service_healthy` for `db` and `redis`. This prevents the `api` and `worker` containers from starting before the database and message broker are fully ready to accept connections, preventing crash loops.

## 5. Reverse Proxy
The `nginx` container sits at port 80 and proxies traffic to the internal `api` container at port 8000. This is a common industry practice to handle SSL termination, rate limiting, or load balancing before traffic hits the application server.
