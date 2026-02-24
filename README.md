# 🔬 Microscope Environment

> A simulated microscope environment where an LLM Agent autonomously optimizes microscope parameters to enhance cell image quality. Can also be used as a standalone MCP Server connectable to any local LLM.

---

## What It Does

- **Simulates** a microscope that captures images of cells
- **Evaluates** image quality using metrics (sharpness, contrast, etc.)
- **Optimizes** microscope parameters (laser power, exposure, z-offset) autonomously via an LLM Agent
- **Exposes** a REST API to control the microscope and retrieve results
- **MCP support** — can be used as a standalone MCP Server and connected to any local LLM

---

## Prerequisites

| Tool | Link |
|------|------|
| Ollama Mistral | https://ollama.com/download |
| Claude Desktop | https://claude.com/download |
| Docker | https://www.docker.com/products/docker-desktop/ |

---

## How To (Docker)

### A. With Ollama LLM

```bash
docker-compose up --build full
```

The `llm-agent` executes 15 iterations, autonomously optimizing the microscope environment.

---

### B. With Claude Desktop

**1. Start the server:**
```bash
docker-compose build server
```

**2. Open Claude Desktop**

**3. Add the following config to `claude_desktop_config.json`:**
```json
{
  "mcpServers": {
    "microscope-simulation-server": {
      "command": "docker",
      "args": [run", "--rm", "-i", "ki_inference-server", "python3", "src/edge/mcp/server/mcp_server_microscope_env.py"]
    }
  }
}
```

**4.** Use Claude Desktop to start optimization of the microscope environment.
