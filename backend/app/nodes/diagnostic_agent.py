"""Diagnostic agent - analyzes patient symptoms"""

from app.nodes.diagnostic_agent import DiagnosticAgent

logger = logging.getLogger(__name__)


def diagnostic_node(state: WorkflowState) -> WorkflowState:
    """
    Diagnostic agent analyzes patient symptoms and generates diagnosis
    """
    logger.info(f"Diagnostic agent processing workflow {state.workflow_id}")
    
    if not state.patient_data:
        state.add_error("No patient data for diagnostic")
        return state
    
    try:
        symptoms = state.patient_data.symptoms
        vitals = state.patient_data.vitals
        
        # Simple rule-based diagnostic logic (can be replaced with LLM)
        diagnosis = _analyze_symptoms(symptoms, vitals)
        confidence = _calculate_confidence(symptoms, vitals)
        
        # Generate differential diagnoses
        differential = _get_differential_diagnoses(symptoms)
        
        # Recommend tests
        recommended_tests = _recommend_tests(symptoms, diagnosis)
        
        state.diagnostic_result = DiagnosticResult(
            diagnosis=diagnosis,
            confidence=confidence,
            reasoning=f"Analysis of {len(symptoms)} symptoms with vitals {vitals}",
            differential_diagnoses=differential,
            recommended_tests=recommended_tests
        )
        
        logger.info(f"Diagnostic completed: {diagnosis} (confidence: {confidence})")
        state.metadata["diagnostic_timestamp"] = datetime.now().isoformat()
        
    except Exception as e:
        logger.error(f"Diagnostic error: {str(e)}")
        state.add_error(f"Diagnostic failed: {str(e)}")
    
    return state


def _analyze_symptoms(symptoms: list, vitals: dict) -> str:
    """Simple symptom analysis"""
    symptom_score = {}
    
    # Map symptoms to conditions (simplified)
    if "fever" in symptoms or "cough" in symptoms:
        symptom_score["respiratory_infection"] = symptom_score.get("respiratory_infection", 0) + 1
    if "fever" in symptoms:
        symptom_score["infection"] = symptom_score.get("infection", 0) + 1
    if "headache" in symptoms or "fatigue" in symptoms:
        symptom_score["general_illness"] = symptom_score.get("general_illness", 0) + 1
    
    # Return top diagnosis
    if symptom_score:
        return max(symptom_score, key=symptom_score.get)
    return "Unknown"


def _calculate_confidence(symptoms: list, vitals: dict) -> float:
    """Calculate diagnostic confidence"""
    confidence = 0.5  # Base confidence
    
    # Increase confidence with more symptoms
    confidence += min(len(symptoms) * 0.1, 0.3)
    
    # Increase confidence if vitals provided
    if vitals:
        confidence += 0.1
    
    return min(confidence, 0.95)


def _get_differential_diagnoses(symptoms: list) -> list:
    """Generate differential diagnoses"""
    differentials = []
    
    if "fever" in symptoms or "cough" in symptoms:
        differentials.extend(["Common Cold", "Influenza", "Bronchitis"])
    if "headache" in symptoms:
        differentials.append("Migraine")
    
    return differentials[:3]  # Return top 3


def _recommend_tests(symptoms: list, diagnosis: str) -> list:
    """Recommend diagnostic tests"""
    tests = []
    
    if "respiratory" in diagnosis.lower():
        tests.extend(["Chest X-ray", "CBC", "Viral Panel"])
    elif "infection" in diagnosis.lower():
        tests.extend(["Blood Culture", "CBC", "Inflammatory Markers"])
    
    return tests