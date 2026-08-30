import os
import time

import docker
import psycopg2

POSTGRES_HOST = "127.0.0.1"
POSTGRES_PORT = 5445
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DB = "inventory"


def wait_for_postgres(timeout=30):
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
            )
            conn.close()
            print("PostgreSQL is ready.")
            return
        except psycopg2.OperationalError:
            time.sleep(0.5)

    raise TimeoutError("PostgreSQL did not become ready")


def is_container_ready(container):
    container.reload()
    return container.status == "running"


def is_container_healthy(container, timeout=30):
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        container.reload()
        status = container.attrs["State"]["Health"]["Status"]
        if status == "healthy":
            print("DB container status is: healthy")
            return True
        print(f"DB container is not healthy. Status: {status}")
        time.sleep(1)
    print(f"DB container did not become healthy within {timeout} seconds")
    return False


def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= stable_duration / interval:
            return True

        time.sleep(interval)
    return False


def start_database_container():
    client = docker.from_env()
    scripts_dir = os.path.abspath("./scripts")
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container '{container_name}' exists. Stopping and removing...")
        existing_container.stop()
        existing_container.remove()
        print(f"Container '{container_name}' exists. Stopped and removed.")
    except docker.errors.NotFound:  # type: ignore
        print(f"Container '{container_name}' does not exist.")

    container_config = {
        "name": container_name,
        "image": "postgres:16.14-alpine3.24",
        "detach": True,
        "ports": {"5432": str(POSTGRES_PORT)},
        "environment": {
            "POSTGRES_USER": POSTGRES_USER,
            "POSTGRES_PASSWORD": POSTGRES_PASSWORD,
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        # "network_mode": "fastapi-development_dev-network",
        "healthcheck": {
            "test": ["CMD-SHELL", "pg_isready -U postgres"],
            "interval": 1000000000,  # 1 second in nanoseconds
            "timeout": 5000000000,
            "retries": 30,
        },
    }

    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(1)

    if not wait_for_stable_status(container):
        raise RuntimeError("Container did not stabilize within the specified time")

    is_container_healthy(container)
    wait_for_postgres()

    print(f"Container '{container_name}' is created.")

    return container
