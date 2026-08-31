# Use Node.js Debian Bookworm slim as base image
FROM node:22-bookworm-slim

# Install Chromium and system dependencies needed for Headless Chrome
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-kacst \
    fonts-freefont-ttf \
    libxss1 \
    dbus \
    dumb-init \
    && rm -rf /var/lib/apt-lists/*

# Set environment variables for Puppeteer / Chromium
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    CHROME_PATH=/usr/bin/chromium \
    NODE_ENV=production \
    CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=true

# Set working directory
WORKDIR /app

# Install chrome-devtools-mcp and supergateway globally
RUN npm install -g chrome-devtools-mcp@latest supergateway@latest

# Expose port for SSE transport
EXPOSE 8000

# Use dumb-init to handle process signals properly
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Launch supergateway with --stdio parameter wrapping chrome-devtools-mcp
CMD ["supergateway", "--stdio", "chrome-devtools-mcp --chrome-arg=--no-sandbox --chrome-arg=--disable-setuid-sandbox --chrome-arg=--disable-dev-shm-usage --chrome-arg=--headless=new", "--port", "8000", "--ssePath", "/sse"]
