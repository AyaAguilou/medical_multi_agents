# Outils pour interagir avec le patient

def ask_patient(question_index: int) -> str:
    """Retourne la question à poser au patient selon l'index"""
    
    questions = [
        "Depuis combien de temps avez-vous ces symptômes ?",
        "Avez-vous de la fièvre ? Si oui, quelle température ?",
        "Avez-vous des difficultés à respirer ?",
        "Avez-vous des douleurs ? Si oui, où et comment ?",
        "Avez-vous d'autres symptômes que vous voulez mentionner ?"
    ]
    
    if question_index < len(questions):
        return questions[question_index]
    else:
        return "Merci, j'ai toutes les informations nécessaires."