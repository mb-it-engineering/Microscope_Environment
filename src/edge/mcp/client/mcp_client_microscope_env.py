import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self, command: list[str]):
        """
        command example:
        ["python", "mcp_server.py"]
        """
        self.command = command
        self.session: ClientSession | None = None
        self._client_cm = None
        self._streams = None

    async def connect(self):
        # command[0] = executable, command[1:] = args
        server_params = StdioServerParameters(
            command=self.command[0],
            args=self.command[1:],
        )

        self._client_cm = stdio_client(server_params)
        read, write = await self._client_cm.__aenter__()

        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        await self.session.initialize()

    async def call_tool(self, tool_name: str, arguments: dict | None = None):
        if self.session is None:
            raise RuntimeError("Session not initialized")

        result = await self.session.call_tool(
            name=tool_name,
            arguments=arguments or {}
        )
        return result.content

    async def close(self):
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self._client_cm:
            await self._client_cm.__aexit__(None, None, None)