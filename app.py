import streamlit as st
import openai
import base64
from dotenv import load_dotenv
import os
import json
import re
import ast

# --- HARDCODED FULL RESET MECHANISM (für EINEN Klick Reset) ---
if st.session_state.get("do_full_reset", False):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state["just_reset"] = True  # Damit mindestens ein Key bleibt
    try:
        st.experimental_rerun()
    except Exception:
        pass

# --- Hilfsfunktionen ---
def robust_json_loads(content):
    content = content.strip()
    if content.startswith("```"):
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1:
            content = content[start:end+1]
    try:
        return json.loads(content)
    except Exception:
        pass
    try:
        fixed = re.sub(r"'([^']*)'", r'"\1"', content)
        return json.loads(fixed)
    except Exception:
        pass
    try:
        return ast.literal_eval(content)
    except Exception:
        pass
    return None

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def image_file_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode()

def get_image_description(image_base64):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in 1-2 sentences for SEO and Print on Demand purposes."},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64," + image_base64}}
                ]
            }
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()

def get_pod_metadata(image_description, platform):
    if platform == "TeePublic":
        prompt = (
            f"Based on this image description: '{image_description}', generate SEO-optimized metadata for TeePublic.\n"
            "- Title: Max. 8 words (English), only the title text, no label, no colon, no quotation marks, no explanations.\n"
            "- Description: Max. 300 characters (English), only the description text, no label, no colon, no quotation marks, no explanations.\n"
            "- Main tag: The single most important keyword for this design, only the keyword, no label, no colon, no quotation marks, no explanations.\n"
            "- Tags: Exactly 8 additional keywords (without the main tag), English, comma separated as JSON array, only the keywords, no label, no explanations.\n"
            "Return only a valid JSON object using double quotes for all keys and values. DO NOT use any Markdown formatting, code blocks, or introduction. Output only the JSON object, nothing else.\n"
            "Example: {\"title\": \"Funny frog meditation\", \"description\": \"A cute meditating frog...\", \"main_tag\": \"meditation\", \"tags\": [\"frog\", \"yoga\", ...]}"
        )
    elif platform == "Spreadshirt":
        prompt = (
            f"Erstelle Metadaten für Spreadshirt basierend auf dieser Bildbeschreibung: '{image_description}'.\n"
            "- Titel: Max. 50 Zeichen, Deutsch, nur den Titeltext, kein Label, kein Doppelpunkt, keine Anführungszeichen, keine Erklärung.\n"
            "- Beschreibung: Max. 200 Zeichen, Deutsch, nur den Text, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "- Tags: Max. 25 einzelne Wörter, Deutsch, kommasepariert als JSON-Array, keine Labels, keine Erklärung.\n"
            "Gib ausschließlich das JSON-Objekt zurück, nur doppelte Anführungszeichen, KEINE Markdown-Formatierung, KEINE Einleitung, nur das JSON-Objekt.\n"
            "Beispiel: {\"title\": \"Frosch beim Meditieren lustig\", \"description\": \"Ein witziger Frosch meditiert entspannt...\", \"tags\": [\"Frosch\", \"Meditation\", ...]}"
        )
    elif platform == "Redbubble":
        prompt = (
            f"Erstelle Metadaten für Redbubble basierend auf dieser Bildbeschreibung: '{image_description}'.\n"
            "- Titel: Max. 8 Wörter, Deutsch, nur den Titeltext, kein Label, kein Doppelpunkt, keine Anführungszeichen, keine Erklärung.\n"
            "- Beschreibung: Max. 300 Zeichen, Deutsch, nur den Text, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "- Tags: Genau 15 einzelne Wörter, Deutsch, kommasepariert als JSON-Array, keine Labels, keine Erklärung.\n"
            "Gib ausschließlich das JSON-Objekt zurück, nur doppelte Anführungszeichen, KEINE Markdown-Formatierung, KEINE Einleitung, nur das JSON-Objekt.\n"
            "Beispiel: {\"title\": \"Meditierender Frosch lustig\", \"description\": \"Ein niedlicher Frosch sitzt entspannt...\", \"tags\": [\"Frosch\", \"Meditation\", ...]}"
        )
    elif platform == "Amazon Merch":
        prompt = (
            f"Erstelle Metadaten für Amazon Merch basierend auf dieser Bildbeschreibung: '{image_description}'.\n"
            "- Titel: Max. 60 Zeichen, Deutsch, keine Wörter wie 'Shirt' oder 'T-Shirt', nur den Titeltext, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "- Brand Name: Max. 50 Zeichen, Deutsch, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "- Bullet Point 1: Max. 256 Zeichen, Deutsch, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "- Bullet Point 2: Max. 256 Zeichen, Deutsch, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "- Produktbeschreibung: Max. 1900 Zeichen, Deutsch, kein Label, kein Doppelpunkt, keine Erklärung.\n"
            "Gib ausschließlich das JSON-Objekt zurück, nur doppelte Anführungszeichen, KEINE Markdown-Formatierung, KEINE Einleitung, nur das JSON-Objekt.\n"
            "Beispiel: {\"title\": \"Lustiges Meditationsmotiv Frosch\", \"brand\": \"Frosch Design\", \"bullet1\": \"Witziges Geschenk für Yoga Fans...\", \"bullet2\": \"Tolles Motiv für Meditation\", \"description\": \"Niedlicher Frosch beim Meditieren...\"}"
        )
    else:
        prompt = (
            f"Based on this image description: '{image_description}', generate SEO-optimized metadata for a generic Print on Demand platform.\n"
            "Return only a valid JSON object using double quotes for all keys and values. DO NOT use any Markdown formatting, code blocks, or introduction. Output only the JSON object, nothing else."
        )

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in Print on Demand SEO and metadata generation."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    data = robust_json_loads(content)
    if data is None:
        st.warning(f"KI-Antwort konnte nicht geparst werden:\n\n```json\n{content}\n```")
        if platform == "TeePublic":
            data = {
                "title": "",
                "description": "",
                "main_tag": "",
                "tags": []
            }
        elif platform == "Spreadshirt":
            data = {
                "title": "",
                "description": "",
                "tags": []
            }
        elif platform == "Amazon Merch":
            data = {
                "title": "",
                "brand": "",
                "bullet1": "",
                "bullet2": "",
                "description": ""
            }
        else:
            data = {
                "title": "",
                "description": "",
                "tags": []
            }
    return data

# --- Initialisiere Session-State wie gehabt ---
if "metadata_ready" not in st.session_state:
    st.session_state.metadata_ready = False
if "metadata_results" not in st.session_state:
    st.session_state.metadata_results = {}
if "image_description" not in st.session_state:
    st.session_state.image_description = ""
if "image_bytes" not in st.session_state:
    st.session_state.image_bytes = None
if "selected_platforms" not in st.session_state:
    st.session_state.selected_platforms = []

st.markdown("""
    <style>
        .stImage > img { border-radius: 16px; max-height: 135px; }
        .stTextInput, .stTextArea { margin-bottom: 8px; }
        .stTabs [role=tab] { font-size: 1.07em; }
        .stButton { margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("POD Metadaten-Generator")

if not st.session_state.metadata_ready:
    uploaded_file = st.file_uploader("Bild hochladen", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        st.session_state.image_bytes = uploaded_file.read()
        st.image(st.session_state.image_bytes, caption="Dein hochgeladenes Bild", use_container_width=True)
        st.success("Bild erfolgreich hochgeladen!")

        st.write("Plattformen auswählen:")
        platforms = ["TeePublic", "Redbubble", "Spreadshirt", "Amazon Merch"]
        selected_platforms = []
        cols = st.columns(len(platforms))
        for i, platform in enumerate(platforms):
            if cols[i].checkbox(platform, key=f"pl_{platform}", value=(platform=="TeePublic")):
                selected_platforms.append(platform)

        if selected_platforms and st.button("Go"):
            image_base64 = image_file_to_base64(st.session_state.image_bytes)
            with st.spinner("Bild wird analysiert und Metadaten generiert..."):
                image_description = get_image_description(image_base64)
                st.session_state.image_description = image_description
                metadata_results = {}
                for platform in selected_platforms:
                    metadata_results[platform] = get_pod_metadata(image_description, platform)
                st.session_state.selected_platforms = selected_platforms
                st.session_state.metadata_results = metadata_results
                st.session_state.metadata_ready = True

if st.session_state.metadata_ready:
    st.success("Bild erfolgreich hochgeladen!")
    st.success(f"Bildbeschreibung: {st.session_state.image_description}")

    tabs = st.tabs(st.session_state.selected_platforms)
    for i, platform in enumerate(st.session_state.selected_platforms):
        with tabs[i]:
            st.subheader(f"Metadaten für {platform}")
            metadata = st.session_state.metadata_results.get(platform, {})

            if platform == "TeePublic":
                st.text_input("Titel", value=metadata.get("title", ""), key=f"title_{platform}")
                st.text_area("Beschreibung", value=metadata.get("description", ""), key=f"desc_{platform}")
                st.text_input("Main Tag", value=metadata.get("main_tag", ""), key=f"main_tag_{platform}")
                st.text_input("Tags", value=", ".join(metadata.get("tags", [])), key=f"tags_{platform}")
            elif platform == "Spreadshirt":
                st.text_input("Titel", value=metadata.get("title", ""), key=f"title_{platform}")
                st.text_area("Beschreibung", value=metadata.get("description", ""), key=f"desc_{platform}")
                st.text_input("Tags", value=", ".join(metadata.get("tags", [])), key=f"tags_{platform}")
            elif platform == "Amazon Merch":
                st.text_input("Titel", value=metadata.get("title", ""), key=f"title_{platform}")
                st.text_input("Brand Name", value=metadata.get("brand", ""), key=f"brand_{platform}")
                st.text_area("Bullet Point 1", value=metadata.get("bullet1", ""), key=f"bullet1_{platform}")
                st.text_area("Bullet Point 2", value=metadata.get("bullet2", ""), key=f"bullet2_{platform}")
                st.text_area("Produktbeschreibung", value=metadata.get("description", ""), key=f"desc_{platform}")
            else:
                st.text_input("Titel", value=metadata.get("title", ""), key=f"title_{platform}")
                st.text_area("Beschreibung", value=metadata.get("description", ""), key=f"desc_{platform}")
                st.text_input("Tags", value=", ".join(metadata.get("tags", [])), key=f"tags_{platform}")
