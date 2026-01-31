import sys
import os
import json
import logging
import traceback
from typing import Any, Dict, List, Optional

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from calender.main import run

# Setup logging to stderr so it doesn't interfere with stdout JSON-RPC
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("mcp_server")

def read_message():
    """Read a JSON-RPC message from stdin."""
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        return json.loads(line)
    except json.JSONDecodeError:
        logger.error("Failed to decode JSON from stdin")
        return None
    except Exception as e:
        logger.error(f"Error reading message: {e}")
        return None

def send_message(msg: Dict[str, Any]):
    """Send a JSON-RPC message to stdout."""
    try:
        json.dump(msg, sys.stdout)
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as e:
        logger.error(f"Error sending message: {e}")

def handle_initialize(request: Dict[str, Any]):
    """Handle the initialize request."""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {
                "listChanged": False
            }
        },
        "serverInfo": {
            "name": "CalendarMCPServer",
            "version": "1.0.0"
        }
    }

def handle_list_tools():
    """Handle the tools/list request."""
    return {
        "tools": [
            {
                "name": "task_and_schedule_planer",
                "description": "Plan and schedule tasks using the calendar crew agent. Use this for ANY task-related request including planning, scheduling, creating, or organizing tasks.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The task description or query from the user"
                        }
                    },
                    "required": ["topic"]
                }
            }
        ]
    }

def handle_call_tool(params: Dict[str, Any]):
    """Handle the tools/call request."""
    name = params.get("name")
    arguments = params.get("arguments", {})

    if name == "task_and_schedule_planer":
        topic = arguments.get("topic")
        if not topic:
             # Fallback: check for 'input' or 'task' or just try to use the whole arguments as context if simpler
             topic = arguments.get("input") or arguments.get("task") or str(arguments)
        
        logger.info(f"Executing task_and_schedule_planer with topic: {topic}")
        
        try:
            # Execute the crew run function
            result = run(topic)
            
            # The result from run() might be complex, ensure it's a string or serializable
            result_str = str(result)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result_str
                    }
                ],
                "isError": False
            }
        except Exception as e:
            logger.error(f"Error executing tool: {traceback.format_exc()}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error executing task: {str(e)}"
                    }
                ],
                "isError": True
            }
    
    raise ValueError(f"Unknown tool: {name}")

def main():
    logger.info("Starting Calendar MCP Server (Stdio)...")
    
    while True:
        request = read_message()
        if request is None:
            break
            
        request_id = request.get("id")
        method = request.get("method")
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id
        }
        
        try:
            if method == "initialize":
                response["result"] = handle_initialize(request)
            elif method == "notifications/initialized":
                # client acknowledging initialization
                logging.info("Client initialized")
                continue # No response needed for notification
            elif method == "tools/list":
                response["result"] = handle_list_tools()
            elif method == "tools/call":
                response["result"] = handle_call_tool(request.get("params", {}))
            else:
                # Handle unknown method or just ignore notifications
                if request_id is not None:
                    response["error"] = {"code": -32601, "message": "Method not found"}
                else:
                    continue # Ignore unknown notifications

        except Exception as e:
            logger.error(f"Error handling request {method}: {e}")
            if request_id is not None:
                response["error"] = {"code": -32000, "message": str(e)}

        if request_id is not None:
            send_message(response)

if __name__ == "__main__":
    main()
