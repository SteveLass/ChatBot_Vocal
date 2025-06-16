import streamlit as st
import nltk
from nltk.chat.util import Chat, reflections
import speech_recognition as sr
import pyttsx3
import threading

# Téléchargement des ressources NLTK
nltk.download('punkt')

# === Texte historique intégré ===
history_text = """
La Côte d'Ivoire a obtenu son indépendance de la France le 7 août 1960. 
Félix Houphouët-Boigny devient le premier président du pays et restera au pouvoir jusqu’à sa mort en 1993. 
Son gouvernement a favorisé une croissance économique rapide, soutenue par l'agriculture, notamment le cacao et le café, tout en maintenant une stabilité politique relative.

Après son décès, Henri Konan Bédié lui succède, mais son mandat est marqué par des tensions ethniques et politiques. 
Un coup d'État militaire a lieu en 1999, mené par le général Robert Guéï, marquant la première rupture de l'ordre constitutionnel.

En 2000, Laurent Gbagbo est élu président mais son élection est contestée. 
Le pays entre dans une crise politique et militaire majeure en 2002, avec une rébellion qui divise le pays en deux : le nord contrôlé par les rebelles, le sud par le gouvernement.

Après plusieurs accords de paix et médiations internationales, une élection présidentielle est organisée en 2010. 
Le second tour oppose Laurent Gbagbo à Alassane Ouattara. 
Les deux camps revendiquent la victoire, entraînant une crise post-électorale violente qui fait plus de 3000 morts. 
En avril 2011, Gbagbo est arrêté et transféré à la CPI, tandis que Ouattara prend effectivement le pouvoir.

Alassane Ouattara est réélu en 2015 puis en 2020. 
Son dernier mandat est marqué par une stabilité relative, un retour de la croissance économique et la réconciliation nationale progressive. 
La Côte d’Ivoire reste aujourd’hui l’une des économies les plus dynamiques d’Afrique de l’Ouest, malgré des défis liés à la cohésion sociale, à la jeunesse et à l’employabilité.

L’histoire politique ivoirienne reste marquée par une alternance de stabilité et de tensions, mais aussi par une résilience remarquable du peuple ivoirien.
"""


   # === PAIRES DE CONVERSATION INTERACTIVES ===
pairs = [
    [r"bonjour|salut|coucou", 
     ["Bonjour ! Ravi de vous retrouver 😊"]],
    
    [r"quel est ton nom ?", 
     ["Je suis votre guide virtuel pour explorer l’histoire politique de la Côte d’Ivoire."]],
    
    [r"comment vas-tu ?", 
     ["Je vais très bien, merci !"]],
    
    [r"au revoir|bye", 
     ["Au revoir ! À bientôt pour de nouvelles découvertes."]],
    
    [r"(.*)indépendance(.*)", 
     ["L’indépendance de la Côte d’Ivoire a été proclamée le 7 août 1960 avec Félix Houphouët-Boigny comme premier président."]],
    
    [r"(.*)houphouët(.*)|houphouet", 
     ["Félix Houphouët-Boigny a dirigé la Côte d’Ivoire pendant 33 ans, marquant le pays par sa politique de stabilité et de développement."]],
    
    [r"(.*)konan(.*)bedié|bedie", 
     ["Henri Konan Bédié a poursuivi l’œuvre de son prédécesseur, mais son mandat a été marqué par des tensions liées à la politique de l'‘ivoirité’."]],
    
    [r"(.*)coup d.*état(.*)1999", 
     ["Le 24 décembre 1999, un coup d’État militaire dirigé par le général Robert Guéï renverse le président Bédié."]],
    
    [r"(.*)guéï|guei", 
     ["Le général Robert Guéï dirige brièvement le pays avant d’être évincé après les élections contestées de 2000."]],
    
    [r"(.*)gagné|gagnant(.*)élection(.*)2000", 
     ["Laurent Gbagbo remporte les élections de 2000 dans un climat de fortes tensions politiques."]],
    
    [r"(.*)gbagbo", 
     ["Laurent Gbagbo a gouverné de 2000 à 2011, une période marquée par une guerre civile et une crise électorale majeure."]],
    
    [r"(.*)rébellion(.*)2002", 
     ["La rébellion de 2002 a divisé le pays entre le nord et le sud, entraînant une longue crise politique et militaire."]],
    
    [r"(.*)élection(.*)2010", 
     ["Les élections de 2010 débouchent sur une grave crise post-électorale opposant Gbagbo à Ouattara."]],
    
    [r"(.*)crise(.*)2010", 
     ["La crise post-électorale de 2010-2011 a causé plus de 3 000 morts et s’est terminée par l’arrestation de Gbagbo."]],
    
    [r"(.*)ouattara", 
     ["Alassane Ouattara est au pouvoir depuis 2011. Son mandat a été marqué par une forte croissance économique et de nombreuses infrastructures."]],
    
    [r"(.*)situation(.*)actuelle|actualité", 
     ["Le pays poursuit son développement mais doit relever des défis en matière de cohésion sociale, de sécurité et de gouvernance."]],
    
    [r"(.*)résumé|récapitulatif|histoire(.*)", 
     ["Voici un résumé : 1960 : Indépendance — 1993 : Bédié — 1999 : Coup d’État — 2000 : Gbagbo — 2002 : Rébellion — 2010 : Crise post-électorale — Depuis 2011 : Ouattara."]],
    
    # Réponse par défaut quand rien ne correspond
    [r"(.*)", 
     ["Je ne suis pas sûr de comprendre. Essayez avec des mots comme : bonjour, nom, Houphouët, Bédié, coup d’État, Guéï, Gbagbo, rébellion, élections 2000 ou 2010, crise post-électorale, Ouattara, situation actuelle, histoire, résumé..."]]
]



chatbot = Chat(pairs, reflections)

# === Synthèse vocale ===
def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        for voice in engine.getProperty('voices'):
            if "fr" in voice.languages or "french" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run).start()

# === Reconnaissance vocale ===
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
        return "❓ Je n'ai pas compris ce que vous avez dit."
    except sr.RequestError:
        return "❌ Erreur avec le service de reconnaissance vocale."
    except Exception as e:
        return f"Erreur : {str(e)}"

# === Interface Streamlit ===
st.set_page_config(page_title="Chatbot Histoire CI", page_icon="🤖")
st.title("🤖 Chatbot - Histoire de la Côte d'Ivoire 🇨🇮")

st.write("Posez une question sur l’histoire politique ivoirienne. Vous pouvez écrire ou parler.")

mode = st.radio("Choisissez le mode d'entrée :", ["Texte", "Voix"])

if "history" not in st.session_state:
    st.session_state.history = []

# === Mode Texte ===
if mode == "Texte":
    user_input = st.text_input("Vous :", "")
    if user_input:
        response = chatbot.respond(user_input)
        st.session_state.history.append(("Vous", user_input))
        st.session_state.history.append(("Bot", response))
        speak(response)

# === Mode Voix ===
elif mode == "Voix":
    if st.button("🎙️ Cliquer pour parler"):
        user_input = speech_to_text()
        response = chatbot.respond(user_input)
        st.session_state.history.append(("Vous (voix)", user_input))
        st.session_state.history.append(("Bot", response))
        speak(response)

# === Affichage de l'historique ===
st.markdown("---")
for speaker, message in st.session_state.history:
    st.markdown(f"**{speaker}** : {message}")
