# Lux Stock Checker

Este proyecto contiene un script de Python que monitoriza la disponibilidad de un producto y notifica a través de Telegram.

## Funcionalidades

- **Monitorización de Stock:** Comprueba si un producto está disponible, esperando un tiempo aleatorio entre 178 y 499 segundos entre cada comprobación para evitar patrones predecibles.
- **Alertas por Telegram:** Envía un mensaje al canal de Telegram configurado cuando el producto está en stock o cuando se produce un error.
- **Actualización de Descripción del Canal:** Actualiza la descripción del canal de Telegram con el estado actual del stock (`¡EN STOCK!`, `Agotado` o `Error de conexión`) y la hora de la última comprobación.


## Configuración

### 1. Configuración de Telegram

#### Obtener el Token del Bot y el ID del Canal

Para configurar el bot de Telegram, necesitarás dos datos clave: el **Token del Bot** y el **ID del Canal**.

1.  **Crear un Bot y Obtener el Token:**
    *   Abre Telegram y busca a [@BotFather](https://t.me/BotFather).
    *   Inicia un chat con él y usa el comando `/newbot`.
    *   Sigue las instrucciones para elegir un nombre y un nombre de usuario para tu bot.
    *   Una vez creado, BotFather te proporcionará un **Token HTTP API**. Este es tu `TELEGRAM_BOT_TOKEN`.

2.  **Obtener el ID del Canal (`chat_id`):**
    *   Crea un nuevo canal en Telegram (o usa uno existente).
    *   **Añade tu bot** como administrador del canal. Es crucial que el bot tenga permisos para "Enviar mensajes" y "Cambiar la información del canal".
    *   Envía un mensaje cualquiera al canal.
Reenvía ese mensaje desde el canal a [@get_id_bot](https://t.me/get_id_bot).
    *   @get_id_bot te responderá con el `chat_id` del canal. Asegúrate de usar el ID que empieza por `-100`.

Para que el script funcione, el bot de Telegram debe tener los siguientes permisos en el canal:

- **Enviar mensajes:** Para notificar cuando el producto está disponible.
- **Cambiar la información del canal:** Para actualizar la descripción del canal con el estado del stock.

Asegúrate de que tu bot es administrador del canal y tiene ambos permisos activados.

### 2. Publicar en GitHub Container Registry (Imagen Multi-Arquitectura)

Para asegurar la compatibilidad con diferentes arquitecturas de CPU (como Apple Silicon y Synology NAS), la imagen de Docker debe ser construida para múltiples plataformas.

1.  **Inicia sesión en `ghcr.io`:**
    Necesitarás un [Personal Access Token (PAT)](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) con el permiso `write:packages`.
    ```bash
    docker login ghcr.io -u TU_USUARIO_DE_GITHUB -p TU_PAT
    ```

2.  **Crea y activa un nuevo constructor de `buildx` (si es la primera vez):**
    ```bash
    docker buildx create --name mybuilder --use
    ```

3.  **Construye y sube la imagen multi-arquitectura:**
    Este comando construirá la imagen para `linux/amd64` (para tu NAS) y `linux/arm64` (para Apple Silicon) y la subirá directamente al registro.
    ```bash
    docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/ivanmzcom/luxwatch:latest --push .
    ```

### 3. Configurar y Ejecutar con Docker Compose

1.  Crea un archivo llamado `docker-compose.yml` con el siguiente contenido.
2.  Reemplaza los valores `TU_TOKEN_AQUI` y `TU_CHAT_ID_AQUI` con tus credenciales.

```yaml
version: '3.8'

services:
  stock-checker:
    image: ghcr.io/ivanmzcom/luxwatch:latest
    container_name: lux-stock-checker
    environment:
      TELEGRAM_BOT_TOKEN: "TU_TOKEN_AQUI"
      TELEGRAM_CHAT_ID: "TU_CHAT_ID_AQUI"
    restart: always
```

3.  Desde el directorio donde creaste el archivo, ejecuta el siguiente comando para iniciar el contenedor:
    ```bash
    docker-compose up -d
    ```

4.  Para detener el servicio, usa:
    ```bash
    docker-compose down
    ```