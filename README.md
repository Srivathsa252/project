# 2022bcd0020-srivathsa: Full-Stack Web Application with Minikube

## Overview
This repository contains a full-stack web application developed as part of a Minikube deployment exercise. The application features a Flask-based backend API that supports CRUD operations and interacts with a PostgreSQL database. The project is containerized using Docker and deployed on Minikube using Kubernetes components, adhering to the naming convention `2022bcd0020-srivathsa`.

- **Backend**: Flask API with endpoints for task management.
- **Database**: PostgreSQL for persistent storage.
- **Container Image**: `2022bcd0020-srivathsa:latest`.
- **Kubernetes Components**: Deployment, ConfigMap, Secret, PersistentVolume, PersistentVolumeClaim, and Service.

## Repository Structure
```
project/
├── app.py                # Flask application with CRUD operations
├── Dockerfile            # Docker configuration for the backend
├── requirements.txt      # Python dependencies
└── k8s/                  # Kubernetes configuration files
    ├── backend-deploy-2022bcd0020-srivathsa.yaml    # Deployment for backend
    ├── db-config-2022bcd0020-srivathsa.yaml         # ConfigMap for database details
    ├── db-secrets-2022bcd0020-srivathsa.yaml        # Secret for credentials
    ├── pv-2022bcd0020-srivathsa.yaml                # PersistentVolume
    ├── pvc-2022bcd0020-srivathsa.yaml               # PersistentVolumeClaim
    ├── postgres-deploy-2022bcd0020-srivathsa.yaml   # Deployment for PostgreSQL
    └── backend-service-2022bcd0020-srivathsa.yaml   # Service for backend
    └── postgres-service-2022bcd0020-srivathsa.yaml  # Service for PostgreSQL
```

## Prerequisites
- **Minikube**: Installed and running (`minikube start`).
- **kubectl**: Installed for Kubernetes management.
- **Docker**: Installed and configured for Minikube.
- **PowerShell**: For Windows-based commands (adjust for other shells if needed).
- **Git**: To clone and manage the repository.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/2022bcd0020-srivathsa.git
cd 2022bcd0020-srivathsa
```

### 2. Build the Docker Image
Ensure Minikube's Docker environment is active:
```powershell
& minikube -p minikube docker-env | Invoke-Expression
docker build -t 2022bcd0020-srivathsa:latest .
```
Verify the image:
```powershell
docker images
```

### 3. Deploy to Minikube
Apply all Kubernetes configurations:
```powershell
cd k8s
kubectl apply -f .
```

### 4. Verify Deployment
Monitor pod status:
```powershell
kubectl get pods -w
```
Expected output should show:
- `backend-deploy-2022bcd0020-srivathsa-<pod-id>`: `1/1 Running`
- `postgres-deploy-2022bcd0020-<pod-id>`: `1/1 Running`

Check services:
```powershell
kubectl get services
```
Confirm `backend-service-2022bcd0020-srivathsa` and `postgres-service-2022bcd0020-srivathsa` are listed.

### 5. Access the Application
Get the backend service URL:
```powershell
minikube service backend-service-2022bcd0020-srivathsa --url
```
- Expected URL: `http://127.0.0.1:52907` (keep terminal open due to Docker driver on Windows).

## Usage
### Test the API
Use `curl` to test CRUD operations:
- **Create a Task**:
  ```powershell
  curl -X POST -H "Content-Type: application/json" -d "{`"title`":`"Task 1`",`"description`":`"Do something`"}" "http://127.0.0.1:52907/tasks"
  ```
  - Expected response: `{"id": 1, "title": "Task 1", "description": "Do something"}`

- **Get All Tasks**:
  ```powershell
  curl "http://127.0.0.1:52907/tasks"
  ```

- **Update a Task**:
  ```powershell
  curl -X PUT -H "Content-Type: application/json" -d "{`"title`":`"Updated Task`",`"description`":`"Updated description`"}" "http://127.0.0.1:52907/tasks/1"
  ```

- **Delete a Task**:
  ```powershell
  curl -X DELETE "http://127.0.0.1:52907/tasks/1"
  ```

### Alternative with PowerShell
```powershell
Invoke-RestMethod -Method Post -Headers @{"Content-Type"="application/json"} -Body "{`"title`":`"Task 1`",`"description`":`"Do something`"}" -Uri "http://127.0.0.1:52907/tasks"
```

## Troubleshooting
### Common Issues and Fixes
- **ImagePullBackOff**:
  - Ensure the image is built in Minikube's Docker environment: `& minikube -p minikube docker-env | Invoke-Expression` followed by `docker build`.
- **CrashLoopBackOff**:
  - Check logs: `kubectl logs <pod-name>`.
  - Verify Secret (`db-secrets-2022bcd0020-srivathsa`) and ConfigMap (`db-config-2022bcd0020-srivathsa`) are applied.
- **404 Not Found**:
  - Ensure service ports match (`TargetPort: 5000` in service, `containerPort: 5000` in deployment).
  - Check app logs for startup issues: `kubectl logs <pod-name>`.
- **Host Resolution Error**:
  - Ensure `postgres-service-2022bcd0020-srivathsa` service exists: `kubectl get services`.
  - Update `DB_HOST` in `db-config-2022bcd0020-srivathsa.yaml` if mismatched, then reapply and restart the pod.

### Debug Mode
- Enable debug in `app.py`:
  ```python
  app.run(host='0.0.0.0', port=5000, debug=True)
  ```
- Rebuild and redeploy:
  ```powershell
  docker build -t 2022bcd0020-srivathsa:latest .
  kubectl apply -f k8s/backend-deploy-2022bcd0020-srivathsa.yaml
  kubectl delete pod <old-pod-name>
  ```

## Kubernetes Components
- **Deployment**: `backend-deploy-2022bcd0020-srivathsa` (1 replica, image: `2022bcd0020-srivathsa:latest`).
- **ConfigMap**: `db-config-2022bcd0020-srivathsa` (contains `DB_HOST`, `DB_NAME`, `DB_PORT`).
- **Secret**: `db-secrets-2022bcd0020-srivathsa` (contains `DB_USER`, `DB_PASSWORD`).
- **PersistentVolume**: `pv-2022bcd0020-srivathsa` (1Gi storage).
- **PersistentVolumeClaim**: `pvc-2022bcd0020-srivathsa` (bound to PV).
- **Service**: `backend-service-2022bcd0020-srivathsa` (NodePort: 30407, Port: 5000).
