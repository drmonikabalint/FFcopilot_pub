import streamlit as st
import requests

st.title("Upload a pattern file and run parser")

uploaded = st.file_uploader("Upload a PDF or DOCX file", type=["pdf", "docx"])

# Initialize session_state to store files
if "files_ready" not in st.session_state:
    st.session_state.files_ready = False
    st.session_state.files = {}

if uploaded and st.button("Run parser"):
    with st.spinner("Running your parser..."):
        files = {"file": (uploaded.name, uploaded.getvalue())}
        resp = requests.post("https://ffcopilot-1.onrender.com/process", files=files)

    if resp.status_code == 200:
        data = resp.json()
        if "files" in data:
            st.session_state.files = data["files"]  # persist files in session_state
            st.session_state.files_ready = True
        else:
            st.warning("No files returned by backend.")
    else:
        st.error(f"Error calling backend API: {resp.status_code}")

# Show download buttons only if parser ran successfully
if st.session_state.files_ready:
    for fname, content in st.session_state.files.items():
        st.download_button(
            label=f"Download {fname}",
            data=content,
            file_name=fname,
            mime="text/plain",
            key=f"download_{fname}"  # unique key per file
        )
