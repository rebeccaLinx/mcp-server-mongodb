import argparse
from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from mongodb_client import MongoDBClient

# Initialize FastMCP server
mcp = FastMCP("mcp-server-mongodb")
client = MongoDBClient()

@mcp.tool()
async def get_projects(name: Optional[str] = None, full: bool = False) -> List[Dict[str, Any]]:
    """
    Retrieve all projects by scanning all collections in the database.
    Documents with filter {'type': 'project'} are considered project definitions.

    Args:
        name (str, optional): Filter by project name.
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of project documents.
    """
    try:
        return await client.get_projects(name, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

@mcp.tool()
async def get_assets(project_name: Optional[str] = None, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> Any:
    """
    Retrieve assets from a specific project's collection (collection name = project_name).
    Filter: {'type': 'asset', 'silo': 'Assets'}.

    Args:
        project_name (str): The name of the project collection to query.
        name (str, optional): Filter by asset name.
        limit (int, optional): Maximum number of records to return (default 100).
        skip (int, optional): Number of records to skip (default 0).
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of asset documents from that project.
    """
    if not project_name:
        return "Error: project_name is required."
    try:
        return await client.get_assets(project_name, name, limit, skip, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

@mcp.tool()
async def get_sequences(project_name: Optional[str] = None, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> Any:
    """
    Retrieve sequences from a specific project's collection.
    Filter: {'type': 'sequence'}.

    Args:
        project_name (str): The name of the project collection to query.
        name (str, optional): Filter by sequence name.
        limit (int, optional): Maximum number of records to return (default 100).
        skip (int, optional): Number of records to skip (default 0).
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of sequence documents from that project.
    """
    if not project_name:
        return "Error: project_name is required."
    try:
        return await client.get_sequences(project_name, name, limit, skip, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

@mcp.tool()
async def get_shots(project_name: Optional[str] = None, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> Any:
    """
    Retrieve shots from a specific project's collection.
    Filter: {'type': 'asset', 'silo': 'Shots'}.

    Args:
        project_name (str): The name of the project collection to query.
        name (str, optional): Filter by shot name (e.g., 'Seq01Sh0010').
        limit (int, optional): Maximum number of records to return (default 100).
        skip (int, optional): Number of records to skip (default 0).
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of shot documents from that project.
    """
    if not project_name:
        return "Error: project_name is required."
    try:
        return await client.get_shots(project_name, name, limit, skip, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

@mcp.tool()
async def get_subsets(parent_id: str, project_name: Optional[str] = None, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> Any:
    """
    Retrieve subsets for a given parent (shot or asset) in a specific project.
    Filter: {'type': 'subset', 'parent': parent_id}.

    Args:
        project_name (str): The name of the project collection to query.
        parent_id (str): The MongoDB ObjectId string of the parent (shot or asset).
        name (str, optional): Filter by subset name.
        limit (int, optional): Maximum number of records to return (default 100).
        skip (int, optional): Number of records to skip (default 0).
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of subset documents.
    """
    if not project_name:
        return "Error: project_name is required."
    try:
        return await client.get_subsets(project_name, parent_id, name, limit, skip, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

@mcp.tool()
async def get_versions(subset_id: str, project_name: Optional[str] = None, limit: int = 10, skip: int = 0, full: bool = False) -> Any:
    """
    Retrieve versions for a given subset in a specific project.
    Filter: {'type': 'version', 'parent': subset_id}.

    Args:
        project_name (str): The name of the project collection to query.
        subset_id (str): The MongoDB ObjectId string of the subset.
        limit (int, optional): Maximum number of records to return (default 10, returning latest versions).
        skip (int, optional): Number of records to skip (default 0).
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of version documents.
    """
    if not project_name:
        return "Error: project_name is required."
    try:
        return await client.get_versions(project_name, subset_id, limit, skip, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

@mcp.tool()
async def get_representations(version_id: str, project_name: Optional[str] = None, limit: int = 50, skip: int = 0, full: bool = False) -> Any:
    """
    Retrieve all representations for a given version in a specific project.
    Filter: {'type': 'representation', 'parent': version_id}.

    Args:
        project_name (str): The name of the project collection to query.
        version_id (str): The MongoDB ObjectId string of the version.
        limit (int, optional): Maximum number of records to return (default 50).
        skip (int, optional): Number of records to skip (default 0).
        full (bool, optional): If True, return full data including the 'data' field. Defaults to False.

    Returns:
        List[dict]: A list of representation documents.
    """
    if not project_name:
        return "Error: project_name is required."
    try:
        return await client.get_representations(project_name, version_id, limit, skip, full)
    except Exception as e:
        return {"error": "MongoDB Query Error", "message": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Server for MongoDB (Dynamic Collections)")
    parser.add_argument("-host", "--host", type=str, help="MongoDB host address (e.g., 192.168.8.65:27100)", required=True)
    parser.add_argument("-db", "--database", type=str, help="MongoDB database name", default="avalon")
    args = parser.parse_args()
    
    # Initialize the MongoDB connection
    client.setup(args.host, args.database)
    
    # Run the MCP server
    mcp.run(transport="stdio")
