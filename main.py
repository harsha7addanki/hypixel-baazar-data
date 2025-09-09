from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import json
import dotenv; dotenv.load_dotenv()
import os

# Initialize FastMCP server
mcp = FastMCP("hypixel")

# Constants
HYPIXEL_API_BASE = "https://api.hypixel.net"
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")

def get_all_bazaar_data() -> Any:
    """Fetch all bazaar data from Hypixel API."""
    response = httpx.get(f"{HYPIXEL_API_BASE}/v2/skyblock/bazaar", params={"key": HYPIXEL_API_KEY})
    response.raise_for_status()
    return response.json()

def get_specific_item_data(item_id: str) -> Any:
    """Fetch specific item data from Hypixel API."""
    response = httpx.get(f"{HYPIXEL_API_BASE}/v2/skyblock/bazaar", params={"key": HYPIXEL_API_KEY})
    response.raise_for_status()
    data = response.json()
    if item_id not in data["products"]:
        return {"error": "Item not found"}
    return data["products"][item_id]
@mcp.tool()
async def bazaar_data_tool() -> str:
    """
    Tool to fetch all bazaar data.
    
    Args:
        none
    """
    data = get_all_bazaar_data()
    return json.dumps(data)

@mcp.tool()
async def bazaar_specific_tool(item_id: str) -> str:
    """
    Tool to fetch specific bazaar item data.

    Args:
        item_id (str): The ID of the item to fetch.
    """
    data = get_specific_item_data(item_id)
    return json.dumps(data)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
