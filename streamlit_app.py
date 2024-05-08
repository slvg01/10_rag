import time
import streamlit as st
from chain import load_chain


# Custom image for the app icon and the assistant's avatar
company_logo = 'https://www.app.nl/wp-content/uploads/2019/01/Blendle.png'

# Configure streamlit page
st.set_page_config(
    page_title="Company Knowladge Base Chatbot",
    page_icon=company_logo, 
)

# put a title on the page and line return after
st.markdown("""
<h1 style="color: #fc6353;">Company procedures search bot</h1>
<h1 style="color: #fc6353;">Happy to see you again Colleague ❤</h1>
""", unsafe_allow_html=True)

for _ in range(3):
   st.markdown("""
    """)
   
   
# Initialize LLM chain
chain = load_chain()


# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant",
                                  "content": "Hi, I am the Company's smart AI. Ask me anything about the company policies"}]


# Display chat messages from history on app rerun and put a custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Chat logical sequence
#add a base invite message in the chat box 
if query := st.chat_input("Ask me anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant",avatar=company_logo):
        message_placeholder = st.empty()
        # Send user's question to the chain
        result = chain.invoke({"question": query})
        response = result['answer']
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.12)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})