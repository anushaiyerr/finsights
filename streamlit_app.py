import streamlit as st
import tempfile
from gemini_client import GeminiClient

st.title("Finsight")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "csv", "xlsx", "txt"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    st.write("Analyzing file with Gemini... ⏳")
    client = GeminiClient()
    result = client.analyze_file(temp_path)

    st.subheader("Analyzing your results...")
    st.markdown(result)
