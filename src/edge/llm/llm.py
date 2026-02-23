import asyncio
import json
import re
import ollama
from edge.mcp.client.mcp_client_microscope_env import MCPClient
from pathlib import Path
import os

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text()


def extract_json(text: str) -> dict | None:
    """Versucht JSON aus dem Text zu extrahieren, auch wenn Mistral Freitext drumherum schreibt."""
    # Direkt parsen
    try:
        return json.loads(text)
    except Exception:
        pass
    
    # JSON aus Markdown-Codeblock extrahieren
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            pass
    
    # Erstes { ... } im Text suchen
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    
    return None

async def run_agent():
    mcp = MCPClient(["python", "src/edge/mcp/server/mcp_server_microscope_env.py"])
    await mcp.connect()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Start optimizing the microscope. First capture an image to assess the current state."}
    ]
    
    client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))

    for step in range(15):
        print(f"\n--- Step {step + 1} ---")
        
        response = client.chat(
            model="mistral",
            messages=messages,
            options={"temperature": 0}
        )

        content = response["message"]["content"].strip()
        print("LLM:", content)

        action = extract_json(content)
        if action is None:
            print("Invalid JSON. Retrying with reminder...")
            messages.append({
                "role": "user",
                "content": "Your response was not valid JSON. Reply ONLY with raw JSON like: {\"tool\": \"capture_image\", \"args\": {}}"
            })
            continue

        tool_name = action.get("tool")
        args = action.get("args", {})

        if not tool_name:
            print("No tool specified. Stopping.")
            break

        print(f"Calling tool: {tool_name} with args: {args}")
        result = await mcp.call_tool(tool_name, args)
        print("Tool result:", result)

        messages.append({"role": "assistant", "content": content})
        messages.append({
            "role": "user",
            "content": f"Tool result: {json.dumps(result) if isinstance(result, dict) else str(result)}. Continue optimizing."
        })

    await mcp.close()

def main():
    asyncio.run(run_agent())

if __name__ == "__main__":
    asyncio.run(run_agent())