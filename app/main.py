import streamlit as st
from faq import ingest_faq_data, faq_chain
from sql import sql_chain
from smalltalk import talk
from pathlib import Path
from router import router

# --- Page Config and Styled Header ---
st.set_page_config(page_title="E-commerce Chat Assistant", page_icon="🛒", layout="centered")

st.markdown("""
    <div style="background-color:#f9f9f9; padding: 15px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #ddd;">
        <h1 style="color: #2e2e2e; text-align: center; margin: 0; font-size: 28px;">
            🛒 E-commerce Chat Assistant
        </h1>
    </div>
""", unsafe_allow_html=True)

# --- FAQ Data Load ---
faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)

# --- Query Router ---
def ask(query):
    route = router(query).name
    if route == 'faq':
        return faq_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'small_talk':
        return talk(query)
    else:
        return f"❗ Route `{route}` not implemented yet."

# --- Chat Input ---
query = st.chat_input("Type your query here (e.g., refund policy, track order, or say hi)")

# --- Session-based Chat Memory ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    response = ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
