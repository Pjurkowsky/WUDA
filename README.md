# WUDA - Mini Applications Setup

This repository contains two main applications: the back-end (server) and the front-end (user interface). This guide explains how to set up and run them locally.

---

## 🖥️ Back-End Setup

1. **Install dependencies:**
```bash
cd back-end
pip install -r requirements.txt
```
2. Create .env file in backend dir with given values:


```.env
# PostgreSQL database name
POSTGRES_DB=your_database_name

# PostgreSQL user
POSTGRES_USER=your_database_user

# PostgreSQL password
POSTGRES_PASSWORD=your_database_password

# Optional: PostgreSQL host (default is localhost)
POSTGRES_HOST=localhost

# Optional: PostgreSQL port (default is 5432)
PORT=5432

# Secret key for JWT
JWT_KEY=your_secret_jwt_key

```

3. In order to run app use command
``` bash
python3 app.py
```

## 🌐 Front-End Setup

1. **Install dependencies:**
   ```bash
   cd front-end
   pip install -r requirements.txt

2. Create .env file

```.env

# Hostname of the back-end server (default: localhost)
BACKEND_HOSTNAME=localhost

# Port of the back-end server (default: 5000)
BACKEND_PORT=5000

# Secret key for front-end application
SECRET_KEY=your_secret_key_here

# Port where the front-end server will run (default: 8000)
SERVER_PORT=8000
```

3. Run app by following command:


```bash
python3 app.py
```

## Database setup
Required is postgresql. Either run given docker-compose.yaml file or provide setup for backend's `.env` file


```yaml
services:
  postgres:
    image: postgres
    environment:
      POSTGRES_PASSWORD: alamakota
      POSTGRES_USER: board_games
      POSTGRES_DB: games
    ports:
      - 5432:5432
```

## Kubernetes
Deploy helm chart:
```bash
cd charts
helm install app .
```

Check if pods are working:
```bash
kubectl get pods
```
Output should be similiar to:
```bash
NAME                            READY   STATUS    RESTARTS   AGE
app-backend-6f8d54dd7f-jmrkl    1/1     Running   0          20m
app-frontend-8657bb558b-dfr4d   1/1     Running   0          20m
```
