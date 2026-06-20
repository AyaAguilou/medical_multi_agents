def call_mcp(symptom):

    if "fièvre" in symptom.lower():
        return "Repos conseillé et bonne hydratation."

    elif "toux" in symptom.lower():
        return "Surveiller la respiration."

    else:
        return "Consulter un médecin si aggravation."