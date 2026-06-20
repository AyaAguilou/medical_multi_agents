from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .graph import app as graph_app
import requests

api = FastAPI()

# CORS pour permettre au frontend de communiquer avec l'API
api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnswerRequest(BaseModel):
    answer: str

class DoctorRequest(BaseModel):
    comment: str
    approved: bool

# Stockage des sessions
sessions = {}

@api.get("/")
def root():
    return {"message": "API Médicale - Version avec MCP"}

@api.post("/start")
def start():
    """Démarre une consultation"""
    result = graph_app.invoke({
        "question_index": 0,
        "answers": [],
        "doctor_approved": None,
        "pending_doctor": False
    })
    
    session_id = str(len(sessions) + 1)
    sessions[session_id] = result
    
    return {
        "session_id": session_id,
        "question": result.get("current_question", "Début de la consultation"),
        "step": "question"
    }

@api.post("/answer/{session_id}")
def answer(session_id: str, data: AnswerRequest):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    state = sessions[session_id]
    answers = state.get("answers", [])
    answers.append(data.answer)
    state["answers"] = answers
    
    # Exécuter le graphe
    result = graph_app.invoke(state)
    sessions[session_id] = result
    
    # Vérifier si toutes les questions sont posées (5 réponses)
    if len(answers) >= 5:
        # Mettre à jour l'état
        result["all_questions_asked"] = True
        sessions[session_id] = result
        return {
            "step": "doctor",
            "message": "Le médecin doit revoir le dossier"
        }
    
    # Retourner la question suivante
    return {
        "step": "question",
        "question": result.get("current_question", "Terminé"),
        "question_count": len(answers)
    }

@api.post("/doctor/{session_id}")
def doctor_review(session_id: str, data: DoctorRequest):
    """Le médecin valide et donne son avis"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    state = sessions[session_id]
    state["doctor_approved"] = data.approved
    state["doctor_comment"] = data.comment
    
    result = graph_app.invoke(state)
    sessions[session_id] = result
    
    return {
        "step": "complete",
        "report": result.get("report", "")
    }

@api.get("/report/{session_id}")
def get_report(session_id: str):
    """Récupère le rapport final"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    
    state = sessions[session_id]
    return {
        "report": state.get("report", "Rapport non disponible")
    }

# ========== ENDPOINTS MCP ==========

@api.get("/mcp/advice/{symptom}")
def mcp_advice(symptom: str):
    """Appelle l'outil MCP pour obtenir des conseils médicaux"""
    try:
        # Essayer de contacter le serveur MCP s'il tourne
        # Si le serveur MCP n'est pas lancé, on utilise des réponses simulées
        try:
            response = requests.get(f"http://localhost:8001/advice/{symptom}", timeout=2)
            if response.status_code == 200:
                return response.json()
        except:
            # Si MCP ne répond pas, on simule
            pass
        
        # Réponses simulées (fallback)
        symptom_lower = symptom.lower()
        
        advices = {
            "fièvre": "Repos complet, hydratation abondante, paracétamol si température > 38.5°C.",
            "toux": "Repos, hydratation, éviter les efforts physiques. Si persiste > 7 jours, consulter.",
            "douleur": "Repos, application de glace, antalgiques simples. Consulter si la douleur persiste.",
            "fatigue": "Repos, alimentation équilibrée, hydratation. Surveiller l'évolution.",
            "maux de tête": "Repos dans le calme, hydratation, antalgiques légers."
        }
        
        for key in advices:
            if key in symptom_lower:
                return {"advice": advices[key], "source": "simulé"}
        
        return {"advice": "Repos et hydratation. Consulter en cas d'aggravation.", "source": "simulé"}
    
    except Exception as e:
        return {"error": f"Erreur MCP: {str(e)}"}

@api.get("/mcp/redflags/{symptoms}")
def mcp_redflags(symptoms: str):
    """Vérifie les signes d'alerte"""
    red_flags = ["douleur thoracique", "essoufflement", "saignement", "perte de conscience", "paralysie"]
    
    alerts = []
    for flag in red_flags:
        if flag in symptoms.lower():
            alerts.append(flag)
    
    if alerts:
        return {
            "alert": True,
            "signs": alerts,
            "message": f"⚠️ Signes d'alerte détectés: {', '.join(alerts)}. Consultation urgente recommandée."
        }
    
    return {
        "alert": False,
        "message": "Aucun signe d'alerte majeur détecté."
    }

@api.get("/mcp/medication/{condition}")
def mcp_medication(condition: str):
    """Recommande des médicaments pour une condition"""
    meds = {
        "rhume": "Paracétamol 500mg si fièvre, ibuprofène si douleur",
        "grippe": "Paracétamol 500mg, repos, hydratation 2L/jour",
        "allergie": "Antihistaminique (cétirizine 10mg)",
        "mal de tête": "Paracétamol 500mg ou ibuprofène 400mg",
        "toux": "Sirop antitussif, miel, tisane",
        "fièvre": "Paracétamol 500mg toutes 6h, hydratation"
    }
    
    condition_lower = condition.lower()
    for key in meds:
        if key in condition_lower:
            return {
                "condition": condition,
                "medication": meds[key],
                "source": "MCP"
            }
    
    return {
        "condition": condition,
        "medication": "Consultez un médecin pour un traitement adapté.",
        "source": "MCP"
    }
from fastapi.responses import FileResponse
import os

@api.get("/frontend")
async def serve_frontend():
    return FileResponse("frontend/app.py")