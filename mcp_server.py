import sys
import os
import logging
from contextlib import redirect_stdout

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from fastmcp import FastMCP
from calender.main import run

# Setup logging to stderr so it doesn't interfere with stdout JSON-RPC
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("mcp_server")

# Create the FastMCP server instance
mcp = FastMCP("CalendarMCPServer")


@mcp.tool()
def task_and_schedule_planer(topic: str) -> str:
    """
    Plan and schedule tasks using the calendar crew agent.
    Use this for ANY task-related request including planning, scheduling, creating, or organizing tasks.

    Args:
        topic: The task description or query from the user
    """
    logger.info(f"Executing task_and_schedule_planer with topic: {topic}")
    
    try:
        # Execute the crew run function, redirecting stdout to stderr to prevent MCP JSON pollution
        with redirect_stdout(sys.stderr):
            result = run(topic)
        
        # The result from run() might be complex, ensure it's a string
        return str(result)
    except Exception as e:
        logger.error(f"Error executing tool: {e}")
        raise


if __name__ == "__main__":
    logger.info("Starting Calendar MCP Server (FastMCP)...")
    mcp.run()
