# mcp-server-mongodb

A Model Context Protocol (MCP) server for querying MongoDB data, specifically optimized for pipeline databases using the Avalon/OpenPype architecture. This server provides a standardized interface for LLMs to interact with production tracking data.

## Features

- **Dynamic Project Queries**: Automatically handles collections based on project names.
- **Hierarchical Retrieval**: Navigate from Projects to Assets/Shots, Subsets, Versions, and Representations.
- **Asynchronous Operations**: Powered by `motor` for efficient MongoDB interaction.
- **FastMCP Integration**: Leverages the latest MCP standards for seamless tool discovery.

## Tools List (Tools)

| Tool Name | Description | Parameters (**Bold** is required) |
| :--- | :--- | :--- |
| `get_projects` | Retrieve all project definitions from the database | `name`, `full` |
| `get_assets` | Retrieve assets from a specific project's collection | **`project_name`**, `name`, `limit`, `skip`, `full` |
| `get_sequences` | Retrieve sequence information for a project | **`project_name`**, `name`, `limit`, `full` |
| `get_shots` | Retrieve shots (SeqXXShXXXX) within a project | **`project_name`**, `name`, `limit`, `full` |
| `get_subsets` | Retrieve subsets linked to a parent asset or shot | **`project_name`**, **`parent_id`**, `name`, `limit`, `full` |
| `get_versions` | List versions for a given subset | **`project_name`**, **`subset_id`**, `limit`, `full` |
| `get_representations` | Retrieve file representations for a specific version | **`project_name`**, **`version_id`**, `limit`, `full` |

## Installation & Execution

Ensure you have Python 3.11+ and `uv` installed.

```bash
uv sync
```

Run the server via stdio transport:

```bash
uv run main.py -host "YOUR_MONGODB_HOST" -db "YOUR_DATABASE_NAME"
```

### Startup Parameters

| Parameter | Alias | Description | Required |
|-----------|-------|-------------|----------|
| `--host`  | `-host`| MongoDB host address (e.g., `127.0.0.1:27017`) | Yes |
| `--database` | `-db` | MongoDB database name (default: `avalon`) | No |

## Usage Guidelines (Crucial)

When querying production data, the following rules MUST be followed:
1. **Explicit Identification**: The Agent **MUST** be provided with a Project Name, Asset Name, or Shot Name by the user.
2. **No Blind Queries**: Global queries across all projects are strictly forbidden. The Agent must not assume the target project.

## Dependencies

- `mcp`: Model Context Protocol SDK
- `motor`: Asynchronous Python driver for MongoDB
- `pydantic-settings`: Configuration management using Pydantic

## License

MIT
