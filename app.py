import streamlit as st
st.set_page_config(page_title="Mathchat", layout="centered")
st.title("Mathchat")

@st.cache_resource
def create_myagent():
    from agente import agent
    return agent

agent = create_myagent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Digite sua pergunta: ")
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Pensando..."):
        result = agent.invoke({
            "messages": [("user", user_input)]
        })

    response = result["messages"][-1].content

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)