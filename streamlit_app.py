import time
import streamlit as st
from chain import load_chain
import base64


# Custom image for the app icon and the assistant's avatar
company_logo = 'https://www.app.nl/wp-content/uploads/2019/01/Blendle.png'

# Configure streamlit page
st.set_page_config(
    page_title="Company Knowladge Base Chatbot",
    page_icon=company_logo, 
)


# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("style.css")



# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Function to add background image using base64
def add_bg_from_base64(base64_str):
    st.markdown(f"""
         <style>
         .stApp {{
             background-image: url(data:image/jpg;base64,{base64_str});
             background-size: cover;
         }}
         </style>
         """, unsafe_allow_html=True)
    
# Image path
image_path = 'pics/glasses.jpg'

# Convert image to base64
base64_img = image_to_base64(image_path)

# Set background image
add_bg_from_base64(base64_img)






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