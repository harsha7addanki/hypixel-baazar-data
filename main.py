from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import json
import dotenv; dotenv.load_dotenv()
import os
import datetime

# Initialize FastMCP server
mcp = FastMCP("hypixel")

# Constants
HYPIXEL_API_BASE = "https://api.hypixel.net"
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")

# Directory to store past data
PAST_DATA_DIR = "past_data"
os.makedirs(PAST_DATA_DIR, exist_ok=True)

def get_all_bazaar_data() -> Any:
    """Fetch all bazaar data from Hypixel API."""
    response = httpx.get(f"{HYPIXEL_API_BASE}/v2/skyblock/bazaar", params={"key": HYPIXEL_API_KEY})
    response.raise_for_status()
    data = response.json()
    file_path = save_bazaar_data(data)
    return data

def get_specific_item_data(item_id: str) -> Any:
    """Fetch specific item data from Hypixel API."""
    response = httpx.get(f"{HYPIXEL_API_BASE}/v2/skyblock/bazaar", params={"key": HYPIXEL_API_KEY})
    response.raise_for_status()
    data = response.json()
    if item_id not in data["products"]:
        return {"error": "Item not found"}
    return data["products"][item_id]

def save_bazaar_data(data: Any) -> str:
    """Save bazaar data to a timestamped JSON file."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(PAST_DATA_DIR, f"bazaar_data_{timestamp}.json")
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return file_path

def load_bazaar_data(timestamp: str) -> Any:
    """Load bazaar data from a specific timestamped JSON file."""
    file_path = os.path.join(PAST_DATA_DIR, f"bazaar_data_{timestamp}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No data found for timestamp: {timestamp}")
    with open(file_path, "r") as file:
        return json.load(file)

def get_all_timestamps() -> list[str]:
    """Get all available timestamps from the past data directory."""
    files = os.listdir(PAST_DATA_DIR)
    timestamps = [
        file_name.replace("bazaar_data_", "").replace(".json", "")
        for file_name in files
        if file_name.startswith("bazaar_data_") and file_name.endswith(".json")
    ]
    return sorted(timestamps)

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

@mcp.tool()
async def load_bazaar_data_tool(timestamp: str) -> str:
    """
    Tool to load past bazaar data by timestamp.

    Args:
        timestamp (str): The timestamp of the data to load.
    """
    try:
        data = load_bazaar_data(timestamp)
        return json.dumps(data)
    except FileNotFoundError as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_all_timestamps_tool() -> str:
    """
    Tool to get all available timestamps.

    Args:
        none
    """
    timestamps = get_all_timestamps()
    return json.dumps({"timestamps": timestamps})

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
