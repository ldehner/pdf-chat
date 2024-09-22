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

# Run Backend

In `backend` folder:

```bash
fastapi dev main.py
```

