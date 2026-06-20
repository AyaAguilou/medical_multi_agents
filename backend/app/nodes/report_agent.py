def report_agent_node(state: dict) -> dict:
    """Agent qui génère le rapport final structuré"""
    
    # Récupérer toutes les informations
    patient_id = state.get("patient_id", "Non spécifié")
    initial_complaint = state.get("initial_complaint", "Non spécifié")
    diagnostic_summary = state.get("diagnostic_summary", "Non disponible")
    interim_care = state.get("interim_care", "Non disponible")
    physician_treatment = state.get("physician_treatment", "Non disponible")
    
    # Générer le rapport final
    report = f"""
    ========================================
    RAPPORT FINAL DE CONSULTATION
    ========================================
    
    Patient ID: {patient_id}
    Plainte initiale: {initial_complaint}
    
    --- SYNTHÈSE CLINIQUE ---
    {diagnostic_summary}
    
    --- RECOMMANDATION INTERMÉDIAIRE ---
    {interim_care}
    
    --- TRAITEMENT PRESCRIT PAR LE MÉDECIN ---
    {physician_treatment}
    
    --- CONCLUSION ---
    Ce rapport est une synthèse préliminaire.
    Ce système ne remplace pas une consultation médicale.
    
    ========================================
    """
    
    state["final_report"] = report
    state["messages"].append({"role": "assistant", "content": report})
    state["next"] = "FINISH"
    
    return state