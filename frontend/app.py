import streamlit as st

st.set_page_config(page_title="Consultation Médicale", page_icon="🏥", layout="wide")

st.title("🏥 Consultation Médicale IA")
st.caption("Système multi-agents pour l'orientation clinique préliminaire")

# ==================== GESTION D'ÉTAT ====================
if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.answers = []
    st.session_state.question_index = 0
    st.session_state.session_id = None

# ==================== QUESTIONS ====================
QUESTIONS = [
    "1. Depuis combien de temps avez-vous ces symptômes ?",
    "2. Avez-vous de la fièvre ? Si oui, quelle température ?",
    "3. Avez-vous des difficultés à respirer ?",
    "4. Avez-vous des douleurs ? Si oui, où et comment ?",
    "5. Avez-vous d'autres symptômes à mentionner ?"
]

# ==================== ÉCRAN START ====================
if st.session_state.step == "start":
    st.header("📋 Nouvelle Consultation")
    st.write("Répondez à 5 questions pour obtenir une synthèse clinique préliminaire.")
    
    if st.button("🚀 Démarrer la consultation", use_container_width=True):
        st.session_state.step = "question"
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.rerun()

# ==================== ÉCRAN QUESTIONS ====================
elif st.session_state.step == "question":
    idx = st.session_state.question_index
    progress = idx / 5
    st.progress(progress)
    st.write(f"**Question {idx + 1} / 5**")
    
    if idx < 5:
        st.markdown(f"""
        <div style="background: #f0f7fa; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #2E86AB;">
            <h3 style="color: #2E86AB;">❓ {QUESTIONS[idx]}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    answer = st.text_input("Votre réponse", placeholder="Écrivez votre réponse ici...")
    
    if st.button("📤 Envoyer", use_container_width=True):
        if answer.strip():
            st.session_state.answers.append(answer)
            st.session_state.question_index += 1
            
            if st.session_state.question_index >= 5:
                st.session_state.step = "doctor"
            st.rerun()
        else:
            st.warning("⚠️ Veuillez entrer une réponse")

# ==================== ÉCRAN MÉDECIN ====================
elif st.session_state.step == "doctor":
    st.header("👨‍⚕️ Revue Médicale")
    st.info("Le médecin doit valider le dossier avant la génération du rapport final.")
    
    with st.expander("📋 Voir les réponses du patient"):
        for i, ans in enumerate(st.session_state.answers, 1):
            st.write(f"**Question {i}:** {ans}")
    
    comment = st.text_area("Avis du médecin", placeholder="Entrez votre avis médical...")
    approved = st.checkbox("✅ J'approuve le rapport", value=True)
    
    if st.button("📝 Valider et générer le rapport", use_container_width=True):
        st.session_state.doctor_comment = comment
        st.session_state.doctor_approved = approved
        st.session_state.step = "report"
        st.rerun()

# ==================== ÉCRAN RAPPORT ====================
elif st.session_state.step == "report":
    st.header("📄 Rapport Final")
    
    # Générer le rapport
    report = f"""
    RAPPORT FINAL
    
    Synthèse basée sur {len(st.session_state.answers)} réponses.
    
    Réponses du patient:
    {chr(10).join([f'- {a}' for a in st.session_state.answers])}
    
    Avis du médecin: {st.session_state.get('doctor_comment', 'Non fourni')}
    Validation: {'✅ Approuvé' if st.session_state.get('doctor_approved') else '❌ Non approuvé'}
    
    Ce système ne remplace pas une consultation médicale.
    """
    
    st.text_area("Rapport", report, height=300)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Télécharger",
            data=report,
            file_name="rapport_medical.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        if st.button("🔄 Nouvelle consultation", use_container_width=True):
            for key in ["step", "answers", "question_index", "doctor_comment", "doctor_approved"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# ==================== FOOTER ====================
st.divider()
st.caption("Ce système ne remplace pas une consultation médicale.")