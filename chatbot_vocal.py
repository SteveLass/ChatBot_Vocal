import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections

import speech_recognition as sr
import pyttsx3
import threading


# Télécharger les ressources nécessaires
nltk.download('punkt')

# Fonction pour charger et préparer le texte du fichier
def load_histoire(file_path='Histoire.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texte = f.read()
        return texte
    except Exception as e:
        return ""

# Charger le texte
histoire = load_histoire()

# Paires simples basées sur des mots-clés dans le texte
pairs = [
    [r"indépendance|indépendant|1960", ["La Côte d'Ivoire a obtenu son indépendance le 7 août 1960."]],
    [r"président|houphouët-boigny", ["Félix Houphouët-Boigny fut le premier président de la Côte d'Ivoire."]],
    [r"crise|conflit|guerre", ["Le pays a traversé une crise majeure entre 2002 et 2011."]],
    [r"économie|croissance|cacao", ["L'économie ivoirienne repose beaucoup sur le cacao et a connu une croissance importante."]],
    [r"paix|stabilité|reconstruction", ["Depuis 2011, la paix et la stabilité reviennent progressivement en Côte d'Ivoire."]],
    [r"(.*)", ["Je suis désolé, je n'ai pas assez d'informations sur ce sujet. Vous pouvez poser des questions sur l'histoire récente de la Côte d'Ivoire."]]
]

# Création du chatbot
chatbot = Chat(pairs, reflections)

# Configurer Streamlit
st.set_page_config(page_title="Chatbot Histoire Côte d'Ivoire", page_icon="📜")
st.title("📜 Chatbot - Histoire de la Côte d'Ivoire")

st.write("Posez vos questions sur l'histoire récente de la Côte d'Ivoire.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Vous :")

if user_input:
    response = chatbot.respond(user_input)
    st.session_state.history.append(("Vous", user_input))
    st.session_state.history.append(("Bot", response))

st.markdown("---")
for speaker, message in st.session_state.history:
    st.markdown(f"**{speaker}** : {message}")
