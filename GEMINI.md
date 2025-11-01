# Project Overview

This project consists of a Python script designed to monitor the stock of the **signed vinyl from Rosalía's new album 'LUX'** from a Shopify store. The script runs in a continuous loop, checking for stock availability at random intervals between 178 and 499 seconds.

Upon detecting a change in stock status, the script sends a notification to a specified Telegram channel. It also updates the channel's description to reflect the current stock status (e.g., 'IN STOCK!', 'Sold Out', or 'Connection Error') and the timestamp of the last check.

The project is containerized using Docker and orchestrated with Docker Compose, making it easy to deploy and run in a headless environment. It is configured to use an image from the GitHub Container Registry.

## Building and Running

The primary method for running the project is via Docker Compose, which pulls a pre-built image from the GitHub Container Registry.

### Prerequisites

- Docker and Docker Compose must be installed.
- The environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` must be correctly set in the `docker-compose.yml` file.

### Running with Docker Compose

1.  **Start the container:**
    ```bash
    docker-compose up -d
    ```

2.  **Check the logs:**
    ```bash
    docker logs lux-stock-checker
    ```

3.  **Stop the container:**
    ```bash
    docker-compose down
    ```

### Building and Pushing the Image (for development)

If you make changes to the script, you need to build and push a new multi-platform image to the GitHub Container Registry.

1.  **Log in to GitHub Container Registry:**
    ```bash
    docker login ghcr.io -u YOUR_GITHUB_USERNAME -p YOUR_PERSONAL_ACCESS_TOKEN
    ```

2.  **Create and switch to a new `buildx` builder instance (if it's your first time):**
    ```bash
    docker buildx create --name mybuilder --use
    ```

3.  **Build and push the multi-platform image:**
    This command will build the image for `linux/amd64` and `linux/arm64` and push it directly to the registry.
    ```bash
    docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/ivanmzcom/luxwatch:latest --push .
    ```

## Development Conventions

- **Configuration:** All configuration, including sensitive data like API tokens, is managed directly within the `docker-compose.yml` file. This is not a recommended security practice for production environments but is how the project is currently configured.
- **Dependencies:** Python dependencies are managed in `requirements.txt` (currently only `requests`).
- **Containerization:** The `Dockerfile` uses a slim Python 3.9 base image and installs dependencies before running the script.
- **Deployment:** The intended deployment method is via Docker Compose, using an image from `ghcr.io`.
