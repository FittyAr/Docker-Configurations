ARG COMFYUI_IMAGE=yanwk/comfyui-boot:cu130-slim-v2
FROM ${COMFYUI_IMAGE}

USER root

# Crear symlinks para que python y python3 apunten a python3.13
RUN ln -sf /usr/bin/python3.13 /usr/local/bin/python \
    && ln -sf /usr/bin/python3.13 /usr/local/bin/python3

# MCP local oficial de Comfy + CLI que utiliza como motor.
RUN python3.13 -m pip install --no-cache-dir --upgrade \
    "comfy-cli>=1.14.0" \
    "comfy-mcp" \
    && command -v comfy \
    && command -v comfy-mcp \
    && comfy --version \
    && comfy-mcp --version

WORKDIR /root/ComfyUI
