import streamlit as st
import requests
import json
import re
import os

# Set page configuration
st.set_page_config(page_title="DeepSeek Chat", layout="centered")

# Directory for storing chat history
CHAT_HISTORY_DIR = "chat_histories"

# Create directory if it doesn't exist
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

# Function to get the latest DeepSeek model dynamically
def get_latest_deepseek_model():
    """Fetch the latest installed DeepSeek model from Ollama."""
    endpoint = "http://localhost:11434/api/tags"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            models = response.json().get("models", [])
            deepseek_models = [m["name"] for m in models if "deepseek" in m["name"].lower()]
            return deepseek_models[-1] if deepseek_models else None  # Return latest DeepSeek model
    except Exception as e:
        st.error(f"Error fetching DeepSeek models: {str(e)}")
    return None


# Load chat histories (latest first)
def load_chat_histories():
    chat_files = sorted(
        [f for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith('.json')],
        key=lambda f: os.path.getctime(os.path.join(CHAT_HISTORY_DIR, f)),
        reverse=True
    )
    return {f: json.load(open(os.path.join(CHAT_HISTORY_DIR, f))) for f in chat_files}

# Load chat histories
chat_histories = load_chat_histories()
chat_names = [os.path.splitext(f)[0] for f in chat_histories.keys()]  # Remove .json extension

# Initialize session state variables
if "selected_chat" not in st.session_state:
    st.session_state.selected_chat = "New Chat"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_filename" not in st.session_state:
    st.session_state.chat_filename = None

# Sidebar: Create New Chat button
if st.sidebar.button("➕ Create New Chat", key="new_chat_button"):
    st.session_state.chat_history = []  # Reset chat history
    st.session_state.selected_chat = "New Chat"  # Switch dropdown to "New Chat"
    st.session_state.chat_filename = None  # Reset filename
    st.rerun()

# Sidebar: Chat selection dropdown
selected_chat = st.sidebar.selectbox(
    "Select a Chat",
    ["New Chat"] + chat_names,
    index=0 if st.session_state.selected_chat == "New Chat" else chat_names.index(st.session_state.selected_chat) + 1,
    key="chat_selector"
)

# Update session state with selected chat
st.session_state.selected_chat = selected_chat

# Load selected chat history (if not new chat)
if selected_chat != "New Chat":
    st.session_state.chat_history = chat_histories.get(f"{selected_chat}.json", [])
    st.session_state.chat_filename = f"{selected_chat}.json"

# Display chat messages
for message in st.session_state.chat_history:
    st.chat_message(message["role"]).write(message["content"])

latest_model = get_latest_deepseek_model()
# if latest_model:
    

# Input box for new messages
if user_input := st.chat_input("Type your message here..."):
    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Placeholder for response
    response_container = st.chat_message("assistant").empty()

    # Function to stream response
    def stream_response():
        endpoint = "http://localhost:11434/api/generate"
        data = {"model": latest_model, "prompt": user_input, "stream": True}
        
        response_text = ""
        try:
            with requests.post(endpoint, json=data, stream=True) as response:
                if response.status_code == 200:
                    for chunk in response.iter_lines(decode_unicode=True):
                        if chunk:
                            try:
                                chunk_json = json.loads(chunk)
                                if "response" in chunk_json:
                                    clean_text = re.sub(r"</?think>", "", chunk_json["response"])  # Remove <think> tags
                                    response_text += clean_text
                                    response_container.write(response_text.strip())  # Stream update
                            except json.JSONDecodeError:
                                response_container.write("Error: Unable to parse JSON chunk")
                else:
                    response_container.write(f"Error: {response.text}")
        except Exception as e:
            response_container.write(f"Error: {str(e)}")

        return response_text.strip()

    # Get response & update history
    final_response = stream_response()
    st.session_state.chat_history.append({"role": "assistant", "content": final_response})

    # Assign filename if new chat
    if selected_chat == "New Chat":
        if not st.session_state.get("chat_filename"):
            # Generate new filename
            new_filename = f"{user_input[:20]}_{len(os.listdir(CHAT_HISTORY_DIR))}.json"
            st.session_state.chat_filename = new_filename

        # Switch to new chat name in dropdown
        st.session_state.selected_chat = os.path.splitext(st.session_state.chat_filename)[0]

    # Save chat history
    with open(os.path.join(CHAT_HISTORY_DIR, st.session_state.chat_filename), 'w') as file:
        json.dump(st.session_state.chat_history, file)

    st.rerun()