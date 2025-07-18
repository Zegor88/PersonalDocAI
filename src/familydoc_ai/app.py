import streamlit as st
from pathlib import Path
from familydoc_ai.agent import TherapistAgent

# --- App Configuration ---
st.set_page_config(
    page_title="FamilyDocAI Therapist",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- Paths and Constants ---
DATA_PATH = Path(__file__).parent.parent.parent / "data" / "input"

# --- Caching ---
@st.cache_resource
def load_agent() -> TherapistAgent:
    """Loads the TherapistAgent, caching it to improve performance."""
    return TherapistAgent()

# --- Main App Logic ---
st.title("🧠 FamilyDocAI Therapist")
st.caption("Your understanding AI companion, here to listen and support.")

agent = load_agent()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

async def process_message(prompt: str):
    """Process user message asynchronously."""
    response = await agent.run(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.direct_answer)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.direct_answer})

# React to user input
if prompt := st.chat_input("How are you feeling today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("AI is thinking..."):
        import asyncio
        asyncio.run(process_message(prompt)) 