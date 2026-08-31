# Chrome DevTools MCP - Docker Setup

Servidor **Chrome DevTools MCP** empaquetado en Docker con Chromium Headless y transporte dual (**SSE** y **Stdio**).
Permite controlar y automatizar la navegación web vía MCP desde cualquier cliente de IA (Antigravity, Minimax, Opencode, Cursor, Claude Desktop, LibreChat, etc.) a nivel global en todos tus proyectos.

---

## 🚀 Inicio Rápido

### 1. Iniciar el servicio
```bash
cd D:/Docker/chrome-devtools-mcp
docker compose up -d
```

### 2. Verificar el estado
```bash
docker compose ps
docker compose logs -f
```

---

## ⚙️ Configuración para Clientes MCP

### 🌐 Opción A: Modo SSE / HTTP (Recomendado)
El contenedor expone un endpoint SSE en `http://localhost:8000/sse`. No requiere invocar procesos locales.

#### Para Antigravity / AGY / Minimax / Opencode / Cursor:
En tu archivo de configuración de MCP (`mcp_config.json` o settings de la aplicación):

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

---

### 💻 Opción B: Modo Stdio (docker exec)
Si tu cliente MCP requiere transporte por stdin/stdout:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "chrome-devtools-mcp",
        "npx",
        "chrome-devtools-mcp",
        "--chrome-arg=--no-sandbox",
        "--chrome-arg=--disable-dev-shm-usage"
      ]
    }
  }
}
```

---

## 🛠️ Opciones y Parámetros del Servidor

Puedes modificar el comando en el `Dockerfile` para ajustar opciones como:

* `--slim`: Solo expone herramientas esenciales (navegación, JS y capturas de pantalla).
* `--screenshotFormat=webp`: Optimiza el formato de las imágenes devueltas para reducir tokens.
* `--screenshotMaxWidth=1280`: Limita la resolución máxima de capturas.

Ejemplo en `Dockerfile`:
```dockerfile
CMD ["supergateway", "--port", "8000", "--ssePath", "/sse", "--", "chrome-devtools-mcp", "--chrome-arg=--no-sandbox", "--chrome-arg=--disable-dev-shm-usage", "--screenshotFormat=webp", "--screenshotMaxWidth=1280"]
```

---

## 📋 Comandos Utilitarios

* **Detener contenedor:** `docker compose down`
* **Reiniciar contenedor:** `docker compose restart`
* **Reconstruir imagen:** `docker compose build --no-cache`
