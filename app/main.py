import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(portfolio, clean_text):
    st.title("Cold Mail Generator")

    api_key = st.text_input("Groq API Key:", type="password", help="Get one free at https://console.groq.com")
    url_input = st.text_input("Enter a URL:", value="job url")
    submit_button = st.button("Submit")

    if submit_button:
        if not api_key:
            st.warning("Please enter your Groq API key.")
            return
        try:
            chain = Chain(api_key)
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = chain.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = chain.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    create_streamlit_app(portfolio, clean_text)