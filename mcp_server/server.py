from fastmcp import FastMCP

# Créer le serveur MCP
mcp = FastMCP("Medical Tools")

@mcp.tool()
def get_medical_advice(symptom: str) -> str:
    """Outil MCP : donne des conseils médicaux généraux"""
    
    advices = {
        "fièvre": "Repos, hydratation, paracétamol si > 38.5°C",
        "toux": "Repos, hydratation, éviter les efforts",
        "douleur": "Repos, glace, antalgiques si besoin",
        "fatigue": "Repos, alimentation légère, hydratation"
    }
    
    for key in advices:
        if key in symptom.lower():
            return advices[key]
    
    return "Repos et hydratation. Consulter si aggravation."

@mcp.tool()
def check_red_flags(symptoms: str) -> str:
    """Outil MCP : vérifie les signes d'alerte"""
    
    red_flags = ["douleur thoracique", "essoufflement", "saignement", "perte de conscience"]
    
    for flag in red_flags:
        if flag in symptoms.lower():
            return f"⚠️ ALERTE : {flag} détecté. Consultation urgente recommandée."
    
    return "Aucun signe d'alerte majeur détecté."

@mcp.tool()
def get_medication(condition: str) -> str:
    """Outil MCP : recommande des médicaments courants"""
    
    meds = {
        "rhume": "Paracétamol, ibuprofène",
        "grippe": "Paracétamol, repos, hydratation",
        "allergie": "Antihistaminique (cétirizine)",
        "mal de tête": "Paracétamol, ibuprofène"
    }
    
    for key in meds:
        if key in condition.lower():
            return f"Médicaments recommandés : {meds[key]}"
    
    return "Consultez un médecin pour un traitement adapté."

if __name__ == "__main__":
    mcp.run()