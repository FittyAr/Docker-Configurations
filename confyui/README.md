# ComfyUI + Comfy MCP en Docker Compose

Stack local para NVIDIA que contiene:

- ComfyUI con acceso a GPU.
- Persistencia de modelos, custom nodes, workflows, entradas y salidas.
- `comfy-cli >= 1.14.0`.
- `comfy-mcp`, el MCP local oficial de Comfy.

## 1. Requisitos

- Docker Desktop + WSL2 en Windows, o Docker Engine en Linux.
- Driver NVIDIA actualizado.
- Acceso de Docker a la GPU.

Comprobación rápida:

```powershell
docker run --rm --gpus all nvidia/cuda:12.9.0-base-ubuntu22.04 nvidia-smi
```

## 2. Configuración

En PowerShell:

```powershell
Copy-Item .env.example .env
```

La configuración por defecto usa:

```text
yanwk/comfyui-boot:cu130-slim-v2
```

Para GTX 10xx/Pascal cambiá `.env` a:

```text
COMFYUI_IMAGE=yanwk/comfyui-boot:cu126-slim
```

## 3. Construir y arrancar ComfyUI

```powershell
docker compose build --pull
docker compose up -d comfyui
```

Abrí:

```text
http://localhost:8188
```

Estado:

```powershell
docker compose ps
docker compose logs -f comfyui
```

GPU dentro del contenedor:

```powershell
docker compose exec comfyui nvidia-smi
```

## 4. MCP

El MCP local oficial de Comfy usa **STDIO**. No abre un puerto HTTP propio.
El cliente MCP debe iniciar el proceso y mantener conectados stdin/stdout.

Probar que quedó instalado:

```powershell
docker compose --profile mcp run --rm -T mcp --version
```

Para usarlo desde un cliente MCP, tomá `mcp-client.example.json` y reemplazá:

```text
C:/RUTA/ABSOLUTA/comfyui-mcp-docker/compose.yaml
```

por la ruta absoluta real del archivo `compose.yaml`.

El comando que termina ejecutando el cliente es:

```powershell
docker compose -f C:/ruta/comfyui-mcp-docker/compose.yaml run --rm -T mcp
```

`-T` es importante: evita crear un pseudo-TTY que pueda corromper el protocolo MCP por STDIO.

## 5. Codex

Se incluye `codex-config.example.toml` con el mismo transporte Docker/STDIO.
Ajustá la ruta absoluta del `compose.yaml` antes de usarlo.

## 6. Directorios persistentes

El directorio indicado por `COMFYUI_STORAGE` queda organizado así:

```text
storage/
├── cache/
├── config/
├── local/
├── custom_nodes/
├── models/
├── input/
├── output/
├── user/
└── user-scripts/
```

Por defecto es `./storage`.

En Windows/WSL2, si vas a manejar muchos checkpoints grandes, suele rendir mejor guardar este directorio dentro del filesystem Linux de WSL2 en vez de una carpeta NTFS montada desde `C:`.

## 7. Importante sobre las herramientas MCP de administración

En este stack, el servicio `mcp` es un proceso STDIO separado que controla el ComfyUI del servicio `comfyui` mediante su API en `127.0.0.1:8188` dentro del namespace de red compartido.

Usá MCP para:

- ejecutar workflows;
- subir inputs;
- consultar jobs;
- recuperar outputs;
- inspeccionar modelos/nodos/workflows.

Para arrancar, detener, actualizar o recrear el servidor ComfyUI, preferí Docker Compose:

```powershell
docker compose restart comfyui
docker compose pull
docker compose build --pull
docker compose up -d --force-recreate comfyui
```

Esto evita que las operaciones de lifecycle del MCP intenten gestionar el proceso desde el contenedor auxiliar.

## 8. Actualizar

```powershell
docker compose down
docker compose build --pull --no-cache
docker compose up -d comfyui
```

Los modelos y resultados permanecen en `COMFYUI_STORAGE`.


## Nota sobre la imagen `cu130-slim-v2`

Esta imagen expone Python como `/usr/bin/python3` y no necesariamente crea el alias `python`.
Por eso el Dockerfile usa explícitamente `python3 -m pip` y el healthcheck usa `python3`.

El servicio MCP comparte el namespace de red de `comfyui`, por lo que `127.0.0.1:8188` apunta al mismo servidor ComfyUI y no hace falta definir `COMFYUI_URL`. Esto evita que `comfy-mcp` trate la instancia como un host remoto para operaciones como descargas de modelos.
