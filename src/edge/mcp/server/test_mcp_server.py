import pytest
import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = "src/edge/mcp/server/mcp_server_microscope_env.py"
EXPECTED_TOOLS = [
    "capture_image",
    "set_parameter",
    "set_laser_power_parameter",
    "set_exposure_parameter",
    "set_z_offset_parameter",
    "get_parameters",
    "reset"
]

@pytest.mark.asyncio
async def test_mcp_server_tools():
    """Connect to an MCP server and verify the tools"""

    exit_stack = AsyncExitStack()

    server_params = StdioServerParameters(
        command="python", args=[SERVER_PATH], env=None
    )

    stdio_transport = await exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(
        ClientSession(stdio, write)
    )

    await session.initialize()

    response = await session.list_tools()
    tools = response.tools
    tool_names = [tool.name for tool in tools]
    tool_descriptions = [tool.description for tool in tools]

    print("\nYour server has the following tools:")
    for tool_name, tool_description in zip(tool_names, tool_descriptions):
        print(f"{tool_name}: {tool_description}")

    assert sorted(EXPECTED_TOOLS) == sorted(tool_names)

    await exit_stack.aclose()