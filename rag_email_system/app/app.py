import streamlit as st
from retriever import Retriever

st.set_page_config(page_title="OpenSearch RAG")

st.title("📧 OpenSearch RAG with Embedding Model")

with st.form("search_form"):
    query = st.text_input("Ask a question")
    submitted = st.form_submit_button("Search")

if submitted and query:
    with st.spinner("Thinking..."):
        response = Retriever.answer(query)
    st.success(response)

