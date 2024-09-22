# Setup

## Anaconda

### Create virtual environment

```bash
conda create -n mal2_env python=3.12 anaconda
```

### Activate environment

```bash
conda activate mal2_env
```

## Python

### Install packages

```bash
pip install -r /backend/requirements.txt
```

Here’s a short README with instructions on how to execute, stop, and remove the PostgreSQL Docker container using Docker Compose:

# Run Postgres docker
To start the PostgreSQL container with Docker Compose, run:

```bash
cd /backend/database
docker-compose up -d
```

- **`-d`**: Runs the container in detached mode (in the background).

To stop the container, use:

```bash
docker-compose down
```

This will stop and remove the running container, but it will keep the data in the volume.

To remove the container along with its associated volumes and persistent data, run:

```bash
docker-compose down -v
```

- **`-v`**: This flag removes the volumes, including the PostgreSQL data stored in the volume.

Now you can easily execute, stop, and remove your PostgreSQL Docker container with these commands.

# Run Backend

In `backend` folder:

```bash
fastapi dev main.py
```

