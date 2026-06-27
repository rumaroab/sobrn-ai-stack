# Getting Started

This guide gets SOBRN AI Stack running on your machine with Docker Compose, Ollama, and Open WebUI.

## Requirements

- Docker
- Docker Compose
- Enough disk space for model files

Model downloads can be several gigabytes. Start with a smaller model if you are on a lightweight laptop.

## 1. Clone the Repository

```bash
git clone https://github.com/your-org/sobrn-ai-stack.git
cd sobrn-ai-stack
```

If you already have the repository locally, open a terminal in the project directory.

## 2. Create Your Environment File

```bash
cp .env.example .env
```

The defaults expose:

- Open WebUI on `http://localhost:3000`
- Ollama on `http://localhost:11434`

You can edit `.env` if those ports are already in use.

## 3. Start Docker Compose

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

## 4. Pull a Model

Pull the default starter model:

```bash
./scripts/pull-model.sh
```

Or pass a specific model:

```bash
./scripts/pull-model.sh phi3:mini
```

## 5. Open Open WebUI

Open:

[http://localhost:3000](http://localhost:3000)

Create your local Open WebUI account when prompted. This account is stored in the local Docker volume.

## 6. Check the Stack

```bash
./scripts/healthcheck.sh
```

You should see success messages for both Ollama and Open WebUI.

## Troubleshooting

### Docker Is Not Running

Start Docker Desktop or your Docker service, then run:

```bash
docker compose up -d
```

### Port Already in Use

Edit `.env` and choose different ports:

```bash
OPEN_WEBUI_PORT=3001
OLLAMA_PORT=11435
```

Then restart:

```bash
docker compose down
docker compose up -d
```

### Model Pull Is Slow

Model downloads can be large. Try a smaller model:

```bash
./scripts/pull-model.sh phi3:mini
```

### Open WebUI Cannot See Ollama

Confirm the stack is running:

```bash
docker compose ps
```

Then check that `.env` contains:

```text
OLLAMA_HOST=http://ollama:11434
```

Restart after changes:

```bash
docker compose up -d
```

### Reset Local Data

This removes containers and local volumes, including downloaded models and Open WebUI data:

```bash
docker compose down -v
```
