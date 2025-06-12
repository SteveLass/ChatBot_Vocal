import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections

# Télécharger les ressources nécessaires
nltk.download('punkt')

# Paires de questions-réponses pour le chatbot
pairs = [
    [r"bonjour|salut|coucou", ["Bonjour ! Comment puis-je vous aider ?"]],
    [r"quel est ton nom ?", ["Je suis un chatbot développé avec Python et Streamlit."]],
    [r"comment vas-tu ?", ["Je vais bien, merci ! Et vous ?"]],
    [r"au revoir|bye", ["Au revoir ! Passez une bonne journée."]],
    [r"(.*)", ["Je ne comprends pas bien. Pouvez-vous reformuler ?"]]
]

# Création du chatbot
chatbot = Chat(pairs, reflections)

# Configuration de la page Streamlit
st.set_page_config(page_title="Chatbot Textuel", page_icon="🤖")

st.title("🤖 Chatbot Textuel avec Streamlit")

# Initialiser l'historique si besoin
if "history" not in st.session_state:
    st.session_state.history = []

# Zone de saisie utilisateur
user_input = st.text_input("Vous :")

if user_input:
    # Obtenir la réponse du chatbot
    response = chatbot.respond(user_input)
    # Enregistrer l'échange dans l'historique
    st.session_state.history.append(("Vous", user_input))
    st.session_state.history.append(("Bot", response))

# Afficher l'historique complet de la conversation
st.markdown("---")
for speaker, message in st.session_state.history:
    st.markdown(f"**{speaker}** : {message}")
