"""Workflow execution example for Medical Multi-Agents backend."""

import sys
from pathlib import Path
from typing import Any, Dict

# Make sure the backend package is importable when running this file directly
sys.path.insert(0, str(Path(__file__).parent))

from app.graph import create_workflow, start_workflow, get_workflow_status


def print_workflow_state(state: Dict[str, Any]) -> None:
    """Print a workflow state summary."""
    print("\n=== WORKFLOW STATE ===")
    print(f"Workflow ID: {state.get('workflow_id')}")
    print(f"Phase: {state.get('phase')}")
    print(f"Errors: {state.get('errors')}")
    print(f"Patient ID: {state.get('patient_data', {}).get('patient_id') if state.get('patient_data') else None}")
    print(f"Diagnostic: {state.get('diagnostic_result', {}).get('diagnosis') if state.get('diagnostic_result') else None}")
    print(f"Review approved: {state.get('review_result', {}).get('approved') if state.get('review_result') else None}")
    print(f"Final report status: {state.get('final_report', {}).get('status') if state.get('final_report') else None}")


def run_example_workflow() -> None:
    """Create and execute a workflow from start to finish."""
    workflow_id = create_workflow()
    print(f"Created workflow: {workflow_id}")

    workflow_state = start_workflow(
        workflow_id=workflow_id,
        patient_id="P001",
        symptoms=["fever", "cough", "fatigue"],
        vitals={"temperature": 38.5, "heart_rate": 95}
    )

    print_workflow_state(workflow_state)

    final_state = get_workflow_status(workflow_id)
    print_workflow_state(final_state)


if __name__ == "__main__":
    run_example_workflow()
