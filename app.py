import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("RAG-powered Document Q&A")

# **Upload PDF & Images**
st.subheader("Upload Documents")
uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if st.button("Upload & Process Documents"):
    files = {}
    if uploaded_pdf:
        files["pdf"] = ("uploaded.pdf", uploaded_pdf.getvalue(), "application/pdf")
    if uploaded_image:
        files["image"] = ("uploaded.jpg", uploaded_image.getvalue(), "image/jpeg")

    if not files:
        st.warning("Please upload at least one file.")
    else:
        try:
            response = requests.post(f"{API_URL}/upload/", files=files)
            if response.status_code == 200:
                st.success("Files uploaded and processed successfully!")
                st.session_state["documents_processed"] = True  # Track processing state
            else:
                st.error(f"Error uploading files: {response.text}")
        except Exception as e:
            st.error(f"Upload failed: {str(e)}")

# **Display Themes**
st.subheader("Document Themes")
if "documents_processed" in st.session_state and st.session_state["documents_processed"]:
    response = requests.get(f"{API_URL}/themes/")
    if response.status_code == 200:
        themes_data = response.json().get("themes", [])
        if themes_data:
            st.table(themes_data)
        else:
            st.warning("No themes found.")
    else:
        st.error("Error fetching themes.")

# **Ask Questions**
st.subheader("Ask a Question")
question = st.text_input("Enter your question")

if st.button("Get Answer"):
    if not question:
        st.warning("Please enter a question.")
    elif not st.session_state.get("documents_processed", False):
        st.error("Error: No document data is available. Please upload and process documents first.")
    else:
        try:
            response = requests.post(f"{API_URL}/ask", json={"question": question})
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found.")
                st.write(f"**Answer:** {answer}")
            else:
                st.error(f"Error fetching answer: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")

st.info("Upload PDFs and images, process them, display extracted themes, and then ask questions to retrieve relevant answers.")