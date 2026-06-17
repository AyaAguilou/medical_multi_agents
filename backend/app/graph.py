"""Workflow graph - orchestrates the medical multi-agent workflow"""

import uuid
import logging
from datetime import datetime
from .state import WorkflowState, WorkflowPhase, PatientData
from .nodes.supervisor import supervisor_node
from .nodes.diagnostic_agent import diagnostic_node
from .nodes.physician_review import physician_review_node
from .nodes.report_agent import report_node

logger = logging.getLogger(__name__)

# Store active workflows
_active_workflows = {}


def create_workflow() -> str:
    """Create a new workflow instance"""
    workflow_id = str(uuid.uuid4())
    state = WorkflowState(workflow_id=workflow_id)
    _active_workflows[workflow_id] = state
    logger.info(f"Created workflow {workflow_id}")
    return workflow_id


def start_workflow(workflow_id: str, patient_id: str, symptoms: list, vitals: dict = None) -> dict:
    """
    Start a new medical workflow
    
    Args:
        workflow_id: Unique workflow identifier
        patient_id: Patient identifier
        symptoms: List of patient symptoms
        vitals: Patient vital signs
    
    Returns:
        Workflow state as dictionary
    """
    if workflow_id not in _active_workflows:
        raise ValueError(f"Workflow {workflow_id} not found")
    
    state = _active_workflows[workflow_id]
    
    # Initialize patient data
    state.patient_data = PatientData(
        patient_id=patient_id,
        symptoms=symptoms,
        vitals=vitals or {}
    )
    state.phase = WorkflowPhase.INITIAL
    state.metadata["started_at"] = datetime.now().isoformat()
    
    logger.info(f"Started workflow {workflow_id} for patient {patient_id}")
    
    # Execute workflow
    return execute_workflow(workflow_id)


def execute_workflow(workflow_id: str) -> dict:
    """
    Execute a complete workflow cycle
    
    Args:
        workflow_id: Workflow identifier
    
    Returns:
        Updated workflow state
    """
    if workflow_id not in _active_workflows:
        raise ValueError(f"Workflow {workflow_id} not found")
    
    state = _active_workflows[workflow_id]
    max_iterations = 10
    iteration = 0
    
    while state.phase not in [WorkflowPhase.COMPLETED, WorkflowPhase.FAILED] and iteration < max_iterations:
        iteration += 1
        logger.info(f"Workflow {workflow_id} - Iteration {iteration}, Phase: {state.phase.value}")
        
        # Route based on current phase
        if state.phase == WorkflowPhase.INITIAL:
            state = supervisor_node(state)
        elif state.phase == WorkflowPhase.DIAGNOSTIC:
            state = diagnostic_node(state)
            state = supervisor_node(state)
        elif state.phase == WorkflowPhase.REVIEW:
            state = physician_review_node(state)
            state = supervisor_node(state)
        elif state.phase == WorkflowPhase.REPORT:
            state = report_node(state)
            state = supervisor_node(state)
        else:
            break
    
    if iteration >= max_iterations:
        logger.warning(f"Workflow {workflow_id} reached max iterations")
        state.add_error("Workflow exceeded maximum iterations")
    
    state.metadata["completed_at"] = datetime.now().isoformat()
    state.metadata["iterations"] = iteration
    
    _active_workflows[workflow_id] = state
    return state.to_dict()


def get_workflow_status(workflow_id: str) -> dict:
    """Get current workflow status"""
    if workflow_id not in _active_workflows:
        raise ValueError(f"Workflow {workflow_id} not found")
    
    state = _active_workflows[workflow_id]
    return state.to_dict()


def list_workflows() -> list:
    """List all active workflows"""
    return [
        {
            "workflow_id": wf_id,
            "phase": state.phase.value,
            "patient_id": state.patient_data.patient_id if state.patient_data else None
        }
        for wf_id, state in _active_workflows.items()
    ]
