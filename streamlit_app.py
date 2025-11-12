import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from schema import chatbot
from get_chathistory import save_chat_to_redis, load_chat_from_redis


st.title("Chat with Meisan")
st.write("I'm ready to answer anything related with YTU!")

if 'chat_history' not in st.session_state:
    st.session_state.msg_to_show = []
    st.session_state.chat_history = load_chat_from_redis()

st.write("")
final_text = ""

chat_text=st.chat_input("🙍🏻‍♂️ Enter Your Question...")

if st.session_state.msg_to_show:
    for msg in st.session_state.msg_to_show:
        st.chat_message('user').markdown(msg['human'])
        st.chat_message('assistant').markdown(msg['AI'])

if chat_text:
    final_text = chat_text

if final_text:
    st.chat_message('user').markdown(final_text)
    with st.spinner("Processing..."):
        result = chatbot.invoke({'question': final_text, 'chat_history': st.session_state.chat_history})

    if result:
        # st.write(result)
        st.chat_message('ai').markdown(result['response']['answer'])
        message = {'human': final_text, 'AI': result['response']['answer']}
        st.session_state.msg_to_show.append(message)

        st.session_state.chat_history.append(HumanMessage(content=final_text))
        st.session_state.chat_history.append(AIMessage(content=result['response']['answer']))
    
        save_chat_to_redis(st.session_state.chat_history[-10:])