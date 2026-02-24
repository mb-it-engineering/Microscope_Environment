from mcp.server.fastmcp import FastMCP
import asyncio
import requests
from pathlib import Path

SYSTEM_PROMPT = (Path(__file__).parent / "system_prompt.md").read_text()

mcp = FastMCP("MicroscopeEnv", instructions=SYSTEM_PROMPT)

@mcp.tool()
async def capture_image():
    """ Captures an image and returns the resulting metrics. """
    response = requests.post("http://localhost:8000/execute/capture", json={})
    return response.json()["result"]["metrics"]

@mcp.tool()
async def set_parameter(name: str, value):
    """ Sets a microscope parameter to a given value. """
    response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": name, "value": value})
    return response.json()["result"]

@mcp.tool()
async def set_laser_power_parameter(value):
    """ Sets the laser power parameter to a given value. """
    response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "laser_power", "value": value})
    return response.json()["result"]

@mcp.tool()
async def set_exposure_parameter(value):
    """ Sets the exposure parameter to a given value. """
    response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "exposure", "value": value})
    return response.json()["result"]

@mcp.tool()
async def set_z_offset_parameter(value):
    """ Sets the z_offset parameter to a given value. """
    response = requests.post("http://localhost:8000/execute/set_parameter", json={"name": "z_offset", "value": value})
    return response.json()["result"]

@mcp.tool()
async def get_parameters():
    """ Gets the current microscope parameters. """
    response = requests.post("http://localhost:8000/execute/get_parameters", json={})
    return response.json()["result"]

@mcp.tool()
async def reset():
    """ Resets the microscope environment to its initial state. """
    response = requests.post("http://localhost:8000/execute/reset", json={})
    return response.json()["result"]

if __name__ == "__main__":
    mcp.run(transport="stdio")

def main():
    mcp.run(transport="stdio")