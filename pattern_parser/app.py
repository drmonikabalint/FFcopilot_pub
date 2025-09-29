import streamlit as st
import requests

st.title("Upload a pattern file and run parser")

uploaded = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

if uploaded and st.button("Run parser"):
    with st.spinner("Running your parser..."):
        files = {"file": (uploaded.name, uploaded.getvalue())}
        resp = requests.post("https://ffcopilot-1.onrender.com/", files=files)

    if resp.status_code == 200:
        data = resp.json()
        for fname, content in data["files"].items():
            st.download_button(
                label=f"Download {fname}",
                data=content,
                file_name=fname,
                mime="text/plain",
                key=f"download_{fname}"
            )
    else:
        st.error("Error calling backend API")
