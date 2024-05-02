import time
import streamlit as st
from utils import load_chain
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://www.app.nl/wp-content/uploads/2019/01/Blendle.png'

# Configure streamlit page
st.set_page_config(
    page_title="Your Notion Chatbot",
    page_icon=company_logo, 
    
)
#&nbsp;&nbsp
# put a title on the page
st.markdown("""

<h1 style="text-align: center;color: darkorange;">Happy to see you again ! ❤</h1>

""", unsafe_allow_html=True)

for _ in range(4):
   st.markdown("""
    """)
   
   
# Initialize LLM chain
# llm = OpenAI(client=OpenAI, streaming=True, callbacks=[StreamlitCallbackHandler(message_placeholder)])
chain = load_chain()

# Initialize chat history

if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant",
                                  "content": "Hi Colleague! I am Blendles's smart AI. How can I help you today?"}]


# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user

for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat logic
if query := st.chat_input("Ask me anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant",avatar=company_logo):
        message_placeholder = st.empty()
        # Send user's question to our chain
        result = chain.invoke({"question": query})
        # result = chain.run(input=query)
        # result = st.session_state['chain']({"question": query})
        response = result['answer']
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})