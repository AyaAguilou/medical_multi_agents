"""Report agent - generates final medical report"""

import logging
from datetime import datetime
from ..state import WorkflowState, FinalReport

logger = logging.getLogger(__name__)


def report_node(state: WorkflowState) -> WorkflowState:
    """
    Report agent generates the final medical report
    """
    logger.info(f"Report agent processing workflow {state.workflow_id}")
    
    if not state.diagnostic_result or not state.review_result:
        state.add_error("Missing diagnostic or review results")
        return state
    
    try:
        diagnosis = state.diagnostic_result.diagnosis
        treatment_plan = _generate_treatment_plan(diagnosis, state)
        follow_up = _generate_follow_up(diagnosis)
        
        state.final_report = FinalReport(
            workflow_id=state.workflow_id,
            patient_id=state.patient_data.patient_id,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            follow_up=follow_up,
            created_at=datetime.now().isoformat(),
            reviewed_by="Dr. System",
            status="completed"
        )
        
        logger.info(f"Report generated for patient {state.patient_data.patient_id}")
        state.metadata["report_timestamp"] = datetime.now().isoformat()
        
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        state.add_error(f"Report failed: {str(e)}")
    
    return state


def _generate_treatment_plan(diagnosis: str, state: WorkflowState) -> list:
    """Generate treatment plan based on diagnosis"""
    treatment = []
    
    if "respiratory" in diagnosis.lower():
        treatment.extend([
            "Rest for 3-7 days",
            "Maintain hydration",
            "Monitor symptoms",
            "Seek medical attention if worsens"
        ])
    elif "infection" in diagnosis.lower():
        treatment.extend([
            "Appropriate antibiotics if prescribed",
            "Rest and fluids",
            "Fever management",
            "Follow-up visit in 1 week"
        ])
    else:
        treatment.extend([
            "Monitor symptoms",
            "Rest as needed",
            "Follow-up as recommended"
        ])
    
    return treatment


def _generate_follow_up(diagnosis: str) -> str:
    """Generate follow-up recommendations"""
    if "respiratory" in diagnosis.lower() or "infection" in diagnosis.lower():
        return "7 days"
    return "14 days"