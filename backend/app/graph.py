from langgraph.graph import StateGraph, END

def ask_questions(state):
    idx = state.get("question_index", 0)
    
    questions = [
        "Depuis combien de temps avez-vous ces symptômes ?",
        "Avez-vous de la fièvre ? Si oui, quelle température ?",
        "Avez-vous des difficultés à respirer ?",
        "Avez-vous des douleurs ? Si oui, où et comment ?",
        "Avez-vous d'autres symptômes à mentionner ?"
    ]
    
    if idx < 5:
        state["current_question"] = questions[idx]
        state["question_index"] = idx + 1
    else:
        answers = state.get("answers", [])
        state["diagnosis"] = f"Synthèse basée sur {len(answers)} réponses."
        state["all_questions_asked"] = True
    
    return state

def doctor_review(state):
    if state.get("doctor_approved"):
        state["report"] = f"""
RAPPORT FINAL
Diagnostic: {state.get('diagnosis', 'Non disponible')}
Avis du médecin: {state.get('doctor_comment', 'Non fourni')}
Ce système ne remplace pas une consultation médicale.
"""
        state["next_step"] = "END"
    else:
        state["pending_doctor"] = True
    return state

def router(state):
    if state.get("all_questions_asked"):
        return "doctor"
    if state.get("next_step") == "END":
        return END
    return "ask_questions"

graph = StateGraph(dict)
graph.add_node("ask_questions", ask_questions)
graph.add_node("doctor", doctor_review)

graph.set_entry_point("ask_questions")
graph.add_conditional_edges("ask_questions", router, {
    "ask_questions": "ask_questions",
    "doctor": "doctor",
    END: END
})
graph.add_conditional_edges("doctor", router, {
    END: END
})

app = graph.compile()