FROM mcr.microsoft.com/vscode/devcontainers/typescript-node

WORKDIR /workspace

# Install global tools
RUN npm install -g npm@latest vite

# Copy full project into container for dev use
COPY . .

# Fix permissions (in case you copied with root ownership)
RUN chown -R node:node /workspace
