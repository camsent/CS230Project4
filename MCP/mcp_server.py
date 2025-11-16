import sys
import os

# Add the project root (CS230Project4) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server.fastmcp import FastMCP
import mcp_helper

mcp = FastMCP("Flashcards MCP")

# ---------- USER AUTH ----------
@mcp.tool()
async def register_user(username: str, password: str) -> str:
    """Register a new user."""
    return mcp_helper.register_user(username, password)

@mcp.tool()
async def login_user(username: str, password: str) -> str:
    """Log in a user."""
    return mcp_helper.login_user(username, password)

@mcp.tool()
async def logout_user() -> str:
    """Log out the current user."""
    return mcp_helper.logout_user()


# ---------- FLASHCARDS ----------
@mcp.tool()
async def list_sets() -> str:
    """List all flashcard sets for the current user."""
    return mcp_helper.list_sets()

@mcp.tool()
async def list_flashcards(set_id: str) -> str:
    """List all flashcards in a given set."""
    return mcp_helper.list_flashcards(set_id)

@mcp.tool()
async def create_flashcard_set(title: str) -> str:
    """Create a new flashcard set."""
    return mcp_helper.create_flashcard_set(title)

@mcp.tool()
async def create_flashcard(set_id: str, front: str, back: str) -> str:
    """Create a new flashcard."""
    return mcp_helper.create_flashcard(set_id, front, back)

@mcp.tool()
async def update_flashcard(set_id: str, flashcard_id: str, front: str = None, back: str = None) -> str:
    """Update a flashcard."""
    return mcp_helper.update_flashcard(set_id, flashcard_id, front, back)

@mcp.tool()
async def delete_flashcard(set_id: str, flashcard_id: str) -> str:
    """Delete a flashcard."""
    return mcp_helper.delete_flashcard(set_id, flashcard_id)


# ---------- EXPORT ----------
@mcp.tool()
async def export_flashcards_json() -> str:
    """Export all flashcard sets and flashcards as JSON."""
    return mcp_helper.export_flashcard_sets_to_json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
