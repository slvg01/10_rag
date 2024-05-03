# Create the generative chain for the chatbot

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate


@st.cache_resource
def load_chain():
    """
    The function initializes and configures a conversational retrieval chain to answer user questions.
    It returns a ConversationalRetrievalChain object.
    """

    # Load OpenAI embedding model
    embeddings = OpenAIEmbeddings()

    # Load OpenAI chat model
    llm = ChatOpenAI(temperature=0)

    # Load the local vector database as a retriever
    vector_store = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # Create a memory feature for the chat 
    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history")

    # Create system prompt
    template = """
    You are an AI assistant for answering questions about the Blendle Employee Handbook given to you.
    Below You are given contextual information and a question,  provide a conversational answer.
    Do not build or make up an answer if you do not have supporting information
    If you don't know the answer, just say 'i am very sorry, i do not have any information on that topic yet, please ask your line manager or HR officer directly. 
    If the question is not about the Blendle Employee Handbook, politely inform them that you are tuned to only answer questions about the Blendle Employee Handbook.

    {context}
    Question: {question}
    Answer:"""

    # Create the Conversational Chain
    chain = ConversationalRetrievalChain.from_llm(llm=llm,
                                                  retriever=retriever,
                                                  memory=memory,
                                                  get_chat_history=lambda h: h,
                                                  verbose=True)

    # Add system prompt to chain
    # Can only add it at the end for ConversationalRetrievalChain
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)
    chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate(prompt=QA_CHAIN_PROMPT)

    return chain