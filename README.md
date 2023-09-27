# Tilly


## Installation:
User installation. You will need an environment with *python 3.10*. After that, you can
install the package using `poetry`:

```bash
poetry install
```

### Developer installation:
You will need the development dependencies:
```bash
poetry install --with=dev
```


## Deploy to Azure
**NOTE**: The `sudo` cmds may be necessary to connect to Azure ACR!

```bash
# Set the tenant ID and login to Azure CLI using device code authentication
sudo az login --use-device-code --tenant <tenant ID>

# Set the subscription ID
# Login to the Azure Container Registry
# Check the available tags for the repository
sudo az account set --subscription <sub ID>

sudo az acr login --name acrgovtech
az acr repository show-tags --name acrgovtech --repository acrgovtech

# Set the tag for the Docker image
export TAG=<your_tag>

# Build and tag the Docker image
sudo docker build -t acrgovtech.azurecr.io/acrgovtech:$TAG -f gui/dockerfile .

# Run the Docker image on port 8000
sudo docker run -p 8000:8000 acrgovtech.azurecr.io/acrgovtech:latest

# Push the Docker image to the Azure Container Registry
sudo docker push acrgovtech.azurecr.io/acrgovtech:latest
sudo docker push acrgovtech.azurecr.io/acrgovtech:$TAG

# Restart the Azure Web App with the new version
az webapp restart --name app-govtech --resource-group rg-govtech

# View the logs of the Azure Web App
az webapp log tail --name app-govtech --resource-group rg-govtech
```