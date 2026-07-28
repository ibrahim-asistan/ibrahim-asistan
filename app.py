import os
from google import genai
import streamlit as st

st.set_page_config(page_title="İbrahim Asistan", page_icon="🤖")
st.title("🤖 İbrahim Asistan")

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
  st.error(
      "GEMINI_API_KEY bulunamadı! Lütfen Streamlit Secrets ayarlarına ekleyin."
  )
else:
  client = genai.Client(api_key=api_key)

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("Bir şeyler yazın..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
      response = client.models.generate_content(
    model="gemini-1.5-flash", contents=prompt
)

      bot_response = response.text
    except Exception as e:
      bot_response = f"Bir hata oluştu: {e}"

    with st.chat_message("assistant"):
      st.markdown(bot_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )
