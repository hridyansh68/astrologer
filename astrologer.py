import openai
import streamlit as st


st.title("MeeBaba")

openai.api_key = None

website_url = st.secrets.get("WEB_SITE_URL")

with st.sidebar:
    openai.api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    f"Built by Hridyansh ({website_url})"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "system":
        continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("How can MeeBaba help you?"):

    if not openai.api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if "system_prompt_set" not in st.session_state:
        st.session_state["system_prompt_set"] = True
        system_prompt = f"You are a MeeBaba. Who is an Indian astrologer. This is for fun. Predict a happy future and reply back in a funny way. You have to talk in Hindi. Ask relevant questions that might be needed to predict the made up future."
        st.session_state.messages.append({"role": "system", "content": system_prompt})

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
    full_response = ""
    for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
