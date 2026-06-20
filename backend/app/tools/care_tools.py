# Outils pour les recommandations de soins

def recommend_interim_care(symptoms: str) -> str:
    """Génère une recommandation intermédiaire basée sur les symptômes"""
    
    symptoms_lower = symptoms.lower()
    
    if "fièvre" in symptoms_lower or "fievre" in symptoms_lower:
        return "Repos complet, hydratation abondante (2L/jour), paracétamol si fièvre > 38.5°C. Consulter si aggravation."
    
    elif "douleur" in symptoms_lower or "mal" in symptoms_lower:
        return "Repos, application de glace si douleur localisée, antalgiques simples si besoin. Consulter si la douleur persiste."
    
    elif "toux" in symptoms_lower or "respir" in symptoms_lower:
        return "Repos, hydratation, éviter les efforts physiques. Surveillance de la respiration. Consulter si essoufflement."
    
    else:
        return "Repos et hydratation. Surveillez l'évolution des symptômes. Consultez un médecin en cas d'aggravation."