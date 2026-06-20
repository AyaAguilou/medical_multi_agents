def physician_review_node(state: dict) -> dict:
    """Nœud d'intervention du médecin (Human-in-the-Loop)"""
    
    # Afficher la synthèse au médecin
    summary = state.get("diagnostic_summary", "Synthèse non disponible")
    interim_care = state.get("interim_care", "Recommandation non disponible")
    
    # Message pour le médecin
    review_message = f"""
    REVUE MÉDICALE REQUISE
    
    Synthèse clinique: {summary}
    Recommandation intermédiaire: {interim_care}
    
    Veuillez entrer votre traitement ou conduite à tenir:
    """
    
    state["messages"].append({"role": "system", "content": review_message})
    
    # Le médecin doit fournir un traitement
    if not state.get("physician_treatment"):
        # En attente de l'input du médecin
        state["next"] = "physician_review"
    else:
        # Traitement reçu, continuer
        state["next"] = "supervisor"
    
    return state