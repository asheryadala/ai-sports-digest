import streamlit as st
import requests
import json
import base64

# URLs
n8n_URL = "https://caic-n8n-stage.k8s.stage.ix.statsperform.cloud/webhook/ai.digest"
template_URL = "https://raw.githubusercontent.com/asheryadala/ai-sports-digest/main/SP.template.png"

# Topics
topics = [
    "GenAI in Sports",
    "AI-Powered Technology in Sports",
    "Sports and Technology Innovation",
    "AI and Innovation in Major Sports",
    "AI in Sports Betting",
    "Automated Content Creation in Sports",
    "Computer Vision in Sports",
    "Use of AI in Sports Fan Engagement"
]

# Session state initialization
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "visibility" not in st.session_state:
    st.session_state.visibility = {topic: False for topic in topics}
if "search_topic" not in st.session_state:
    st.session_state.search_topic = ""
if "search_response" not in st.session_state:
    st.session_state.search_response = None
if "search_visible" not in st.session_state:
    st.session_state.search_visible = False

# Background template setup
def set_template(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bg_base64 = base64.b64encode(response.content).decode()
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{bg_base64}");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: scroll;
                    background-position: center;
                    color: white !important;
                    font-family: 'Segoe UI', sans-serif;
                }}
                h1, h2, h3, h4, h5, h6, p, .stMarkdown {{
                    color: white !important;
                }}
                .main > div {{
                    background-color: rgba(0, 0, 0, 0.6);
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
                    max-width: 900px;
                    margin: auto;
                }}
                .stButton > button {{
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: 1px solid white;
                    border-radius: 8px;
                    padding: 0.5rem 1rem;
                    margin: 0.5rem 0;
                    transition: all 0.3s ease;
                }}
                .stButton > button:hover {{
                    background-color: white;
                    color: black;
                }}
                .stTextInput input {{
                    background-color: rgba(0, 0, 0, 0.6) !important;
                    color: white !important;
                    border: 1px solid white !important;
                    caret-color: white !important;
                }}
                .stTextInput input::placeholder {{
                    color: rgba(255, 255, 255, 0.6) !important;
                }}
                label, .stTextInput label {{
                    color: white !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
    except:
        pass

# Webhook request
def get_topic(topic):
    try:
        with st.spinner(f"Getting results for: {topic}..."):
            response = requests.post(n8n_URL, json={"topic": topic}, timeout=15)
            if response.status_code == 200:
                return response.text
            else:
                return "[]"
    except Exception as e:
        return "[]"

# Display results
def get_results(data_text):
    try:
        data = json.loads(data_text)
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, list) and data:
            for item in data:
                st.markdown(f"### {item.get('Title', 'No Title')}")
                st.markdown(f"**Date:** {item.get('Date', 'No Date')}")
                st.markdown(item.get('Summary', 'No Summary'))
                st.markdown(f"[Read more]({item.get('Link', '#')})")
                st.markdown("---")
        else:
            st.warning("No results found.")
    except:
        st.warning("No results found.")

# Set background
set_template(template_URL)

# App title
st.title("⚽ AI Sports Digest")
st.markdown("Stay up to date with the latest AI insights in sports.")
st.markdown("---")

# Topic buttons
for topic in topics:
    if st.button(topic):
        st.session_state.visibility[topic] = not st.session_state.visibility[topic]
        if st.session_state.visibility[topic] and topic not in st.session_state.responses:
            st.session_state.responses[topic] = get_topic(topic)

    if st.session_state.visibility.get(topic) and topic in st.session_state.responses:
        get_results(st.session_state.responses[topic])

# Search section
st.markdown("---")
st.markdown("### 🔍 Search")
search_input = st.text_input("Enter a topic")

if st.button("Search"):
    if search_input:
        st.session_state.search_topic = search_input
        st.session_state.search_visible = True
        st.session_state.search_response = get_topic(search_input)

if st.session_state.search_visible and st.session_state.search_response:
    st.markdown(f"## Results for: _{st.session_state.search_topic}_")
    get_results(st.session_state.search_response)


