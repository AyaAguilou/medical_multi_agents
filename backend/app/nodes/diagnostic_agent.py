def diagnostic_agent_node(state):
    """Agent qui pose des questions et génère une synthèse SANS LLM"""
    
    # Récupérer l'index des questions
    question_index = state.get("question_index", 0)
    
    # Liste des questions
    questions = [
        "Depuis combien de temps avez-vous ces symptômes ?",
        "Avez-vous de la fièvre ? Si oui, quelle température ?",
        "Avez-vous des difficultés à respirer ?",
        "Avez-vous des douleurs ? Si oui, où et comment ?",
        "Avez-vous d'autres symptômes à mentionner ?"
    ]
    
    if question_index < 5:
        # Poser la question
        state["current_question"] = questions[question_index]
        state["question_index"] = question_index + 1
    else:
        # Générer la synthèse à partir des réponses
        answers = state.get("answers", [])
        state["diagnosis"] = f"""
        SYNTHÈSE CLINIQUE PRÉLIMINAIRE
        
        {len(answers)} réponses reçues.
        
        Plaintes du patient:
        {chr(10).join([f'- {a}' for a in answers])}
        
        Recommandation: Repos et hydratation. 
        Consulter un médecin en cas d'aggravation.
        """
        state["all_questions_asked"] = True
    
    return state