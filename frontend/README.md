# JustEat - Premium Food Ordering Platform

A modern food ordering application built with React, TypeScript, and Vite.

## Docker and Azure Web App deployment

This frontend is configured to run as a static SPA behind Nginx.

### 1. Build the image in WSL

From WSL, open the frontend folder and build the container image:

```bash
cd /mnt/c/Assignment/JustEat/frontend
docker build -t justeat-frontend:latest --build-arg VITE_API_BASE_URL=https://YOUR-BACKEND.azurewebsites.net/api .
```

The backend URL is baked into the static build, so rebuild the image if the backend address changes.

### 2. Test the container locally

```bash
docker run --rm -p 8080:80 justeat-frontend:latest
```

Open http://localhost:8080 and confirm the app loads.

### 3. Push the image to Azure Container Registry

```bash
az login
az group create --name justeat-rg --location eastus
az acr create --resource-group justeat-rg --name UNIQUE_ACR_NAME --sku Basic
az acr login --name UNIQUE_ACR_NAME
docker tag justeat-frontend:latest UNIQUE_ACR_NAME.azurecr.io/justeat-frontend:latest
docker push UNIQUE_ACR_NAME.azurecr.io/justeat-frontend:latest
```

### 4. Create the Azure Web App

```bash
az appservice plan create --name justeat-plan --resource-group justeat-rg --is-linux --sku B1
az webapp create --resource-group justeat-rg --plan justeat-plan --name UNIQUE_WEBAPP_NAME --deployment-container-image-name UNIQUE_ACR_NAME.azurecr.io/justeat-frontend:latest
```

### 5. Configure the web app to pull from ACR

```bash
az webapp config container set \
	--resource-group justeat-rg \
	--name UNIQUE_WEBAPP_NAME \
	--docker-custom-image-name UNIQUE_ACR_NAME.azurecr.io/justeat-frontend:latest \
	--docker-registry-server-url https://UNIQUE_ACR_NAME.azurecr.io
```

If Azure asks for registry credentials, use the ACR admin account or a managed identity.

### 6. Backend CORS requirement

Your backend must allow the frontend origin. Set this on the backend app:

```bash
FRONTEND_ORIGINS=https://UNIQUE_WEBAPP_NAME.azurewebsites.net
```

### 7. Browse the app

Open the Azure Web App URL after deployment and verify login, restaurant browsing, and API calls.
