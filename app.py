import streamlit as st
import backend  # Import backend functions

st.title("🔢 AI-Powered Voice Calculator")
st.write("A voice-based AI calculator that understands natural language queries.")

if st.button("🎙️ Start Voice Input"):
    st.write("Listening...")
    backend.main()
    