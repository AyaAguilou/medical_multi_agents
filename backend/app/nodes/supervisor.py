from typing import Literal

def supervisor_node(state: dict) -> dict:
    """Nœud superviseur qui décide de l'étape suivante"""
    
    # Si le rapport final est généré, on termine
    if state.get("final_report"):
        return {"next": "FINISH"}
    
    # Si le médecin a déjà donné son traitement, on va au rapport
    if state.get("physician_treatment"):
        return {"next": "report_agent"}
    
    # Si la synthèse diagnostique est faite, on va vers le médecin
    if state.get("diagnostic_summary"):
        return {"next": "physician_review"}
    
    # Si les 5 questions sont posées, on génère la synthèse
    if state.get("question_count", 0) >= 5:
        return {"next": "diagnostic_agent"}  # Pour générer la synthèse
    
    # Sinon, on continue le diagnostic
    return {"next": "diagnostic_agent"}