import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Load environment variables
load_dotenv()

from calender.main import run

app = FastAPI(title="Calendar Agent API", description="API for scheduling tasks using CrewAI agents.")

class TaskRequest(BaseModel):
    input_task: str

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/run")
async def run_task(request: TaskRequest):
    """
    Run the calendar crew with a given task.
    """
    try:
        # result is likely a string or a CrewOutput object. 
        # API requires a serializable format.
        result = run(request.input_task)
        
        # If result is complex, we might need to str() it or extract logic
        return {"status": "success", "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host=host, port=port)
