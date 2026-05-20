"""Supervisor agent - orchestrates workflow"""

import logging
from datetime import datetime
from ..state import WorkflowState, WorkflowPhase

logger = logging.getLogger(__name__)


def supervisor_node(state: WorkflowState) -> WorkflowState:
    """
    Supervisor agent routes workflow to appropriate agents
    """
    logger.info(f"Supervisor processing workflow {state.workflow_id}")
    
    if state.phase == WorkflowPhase.INITIAL:
        # Validate patient data exists
        if not state.patient_data:
            state.add_error("No patient data provided")
            return state
        
        logger.info(f"Routing patient {state.patient_data.patient_id} to diagnostic agent")
        state.phase = WorkflowPhase.DIAGNOSTIC
        state.metadata["supervisor_timestamp"] = datetime.now().isoformat()
        
    elif state.phase == WorkflowPhase.DIAGNOSTIC:
        # Check if diagnostic completed
        if state.diagnostic_result:
            logger.info("Diagnostic completed, routing to physician review")
            state.phase = WorkflowPhase.REVIEW
        else:
            logger.warning("Diagnostic not completed yet")
    
    elif state.phase == WorkflowPhase.REVIEW:
        # Check if review completed
        if state.review_result:
            if state.review_result.approved:
                logger.info("Diagnosis approved, routing to report generation")
                state.phase = WorkflowPhase.REPORT
            else:
                logger.warning("Diagnosis rejected, routing back to diagnostic")
                state.phase = WorkflowPhase.DIAGNOSTIC
        else:
            logger.warning("Review not completed yet")
    
    elif state.phase == WorkflowPhase.REPORT:
        # Check if report generated
        if state.final_report:
            logger.info("Report completed, workflow finished")
            state.phase = WorkflowPhase.COMPLETED
        else:
            logger.warning("Report not generated yet")
    
    return state