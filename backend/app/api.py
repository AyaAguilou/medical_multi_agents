from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import platform
from .graph import create_workflow, start_workflow, get_workflow_status, list_workflows

app = FastAPI(title="Medical Multi-Agents API", version="1.0.0")


# Request/Response Models
class WorkflowRequest(BaseModel):
    """Request to start a new workflow"""
    patient_id: str
    symptoms: List[str]
    vitals: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    """Workflow response"""
    workflow_id: str
    phase: str
    status: str


@app.get("/")
def home():
    return {"message": "Medical Multi Agent API"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "python": sys.version.splitlines()[0],
        "platform": platform.platform(),
    }


# Workflow endpoints
@app.post("/workflows")
def create_new_workflow() -> dict:
    """Create a new workflow instance"""
    try:
        workflow_id = create_workflow()
        return {
            "workflow_id": workflow_id,
            "status": "created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflows/{workflow_id}/start")
def start_new_workflow(workflow_id: str, request: WorkflowRequest) -> dict:
    """Start a workflow with patient data"""
    try:
        result = start_workflow(
            workflow_id=workflow_id,
            patient_id=request.patient_id,
            symptoms=request.symptoms,
            vitals=request.vitals
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/{workflow_id}")
def get_workflow(workflow_id: str) -> dict:
    """Get workflow status"""
    try:
        result = get_workflow_status(workflow_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows")
def list_all_workflows() -> dict:
    """List all active workflows"""
    try:
        workflows = list_workflows()
        return {
            "count": len(workflows),
            "workflows": workflows
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))