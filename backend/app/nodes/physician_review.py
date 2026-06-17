"""Physician review agent - validates diagnosis"""

import logging
from datetime import datetime
from ..state import WorkflowState, ReviewResult

logger = logging.getLogger(__name__)


def physician_review_node(state: WorkflowState) -> WorkflowState:
    """
    Physician review agent validates diagnosis and provides feedback
    """
    logger.info(f"Physician review processing workflow {state.workflow_id}")
    
    if not state.diagnostic_result:
        state.add_error("No diagnostic result to review")
        return state
    
    try:
        # Simulate physician review
        diagnosis = state.diagnostic_result.diagnosis
        confidence = state.diagnostic_result.confidence
        
        # Approval logic
        approved = confidence >= 0.7
        notes = _generate_review_notes(state)
        
        state.review_result = ReviewResult(
            approved=approved,
            reviewer_notes=notes,
            confidence=confidence,
            modifications=None if approved else "Recommend additional testing"
        )
        
        logger.info(f"Physician review: {'APPROVED' if approved else 'REJECTED'}")
        state.metadata["review_timestamp"] = datetime.now().isoformat()
        state.metadata["reviewer"] = "Dr. System"
        
    except Exception as e:
        logger.error(f"Physician review error: {str(e)}")
        state.add_error(f"Review failed: {str(e)}")
    
    return state


def _generate_review_notes(state: WorkflowState) -> str:
    """Generate physician review notes"""
    diagnostic = state.diagnostic_result
    
    notes = f"""
    Diagnosis: {diagnostic.diagnosis}
    Confidence: {diagnostic.confidence:.1%}
    Reasoning: {diagnostic.reasoning}
    
    Differential Diagnoses:
    - {chr(10).join([f'  {d}' for d in diagnostic.differential_diagnoses])}
    
    Recommended Tests:
    - {chr(10).join([f'  {t}' for t in diagnostic.recommended_tests])}
    
    Patient: {state.patient_data.patient_id}
    Symptoms: {', '.join(state.patient_data.symptoms)}
    """.strip()
    
    return notes