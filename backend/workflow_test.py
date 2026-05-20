from app.nodes.diagnostic_agent import DiagnosticAgent
from app.nodes.physician_review import physician_review
from app.nodes.report_agent import report_agent

# Etat initial
state = {

    "patient_problem": "J'ai de la fièvre et une toux"
}

# Diagnostic
state = diagnostic_agent(state)

print("=== QUESTIONS ===")
print(state["questions"])

print("\n=== RECOMMANDATION ===")
print(state["interim_care"])

print("\n=== SYNTHÈSE ===")
print(state["diagnostic_summary"])

# Human in the loop
state = physician_review(state)

# Rapport final
state = report_agent(state)

print("\n=== RAPPORT FINAL ===")
print(state["final_report"])