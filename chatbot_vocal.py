import streamlit as st
import speech_recognition as sr
import nltk
from nltk.chat.util import Chat, reflections
import pyttsx3
import threading

# Télécharger les ressources NLTK nécessaires
nltk.download('punkt')

# Paires de conversation pour le chatbot
pairs = [
    [r"bonjour|salut|coucou", ["Bonjour ! Comment puis-je vous aider ?"]],
    [r"quel est ton nom ?", ["Je suis un chatbot vocal développé avec Python et Streamlit."]],
    [r"comment vas-tu ?", ["Je vais bien, merci ! Et vous ?"]],
    [r"au revoir|bye", ["Au revoir ! Passez une bonne journée."]],
    [r"(.*)", ["Je ne comprends pas bien. Pouvez-vous reformuler ?"]]
]

# Création du chatbot NLTK
chatbot = Chat(pairs, reflections)

# Fonction pour synthèse vocale en thread (non bloquante)
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        # Choix voix française si disponible
        for voice in engine.getProperty('voices'):
            if "fr" in voice.languages or "french" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# Fonction reconnaissance vocale avec gestion d’erreurs
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("🎤 Parlez maintenant...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        text = recognizer.recognize_google(audio, language="fr-FR")
        return text
    except sr.WaitTimeoutError:
        return "⏱️ Temps d'attente dépassé, veuillez réessayer."
    except sr.UnknownValueError:
        return "Désolé, je n'ai pas compris."
    except sr.RequestError:
        return "Erreur avec le service de reconnaissance vocale."
    except Exception as e:
        return f"Erreur: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Chatbot Vocal", page_icon="🤖")
st.title("🤖 Chatbot Vocal avec Synthèse Vocale")

st.write("💬 Parlez ou écrivez votre message au chatbot.")

mode = st.radio("Choisissez le mode d'entrée :", ["Texte", "Voix"])

if "history" not in st.session_state:
    st.session_state.history = []

# Mode Texte
if mode == "Texte":
    user_input = st.text_input("Vous :", "")
    if user_input:
        response = chatbot.respond(user_input)
        st.session_state.history.append(("Vous", user_input))
        st.session_state.history.append(("Bot", response))
        speak(response)

# Mode Voix
elif mode == "Voix":
    if st.button("🎙️ Cliquer pour parler"):
        user_input = speech_to_text()
        response = chatbot.respond(user_input)
        st.session_state.history.append(("Vous (voix)", user_input))
        st.session_state.history.append(("Bot", response))
        speak(response)

# Affichage historique conversation
st.markdown("---")
for speaker, message in st.session_state.history:
    st.markdown(f"**{speaker}** : {message}")
