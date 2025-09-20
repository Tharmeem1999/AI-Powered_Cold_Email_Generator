import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")   # sets app title
    url_input = st.text_input("Enter a URL:", value="")     # input for career page user
    submit_button = st.button("Submit")     # triggers email generation when clicked

    if submit_button:   # only runs logic after user clicks submit
        try:
            loader = WebBaseLoader([url_input])     # loads webpage content from user-provided URL
            data = clean_text(loader.load().pop().page_content)     # cleans scraped text for LLM readability
            portfolio.load_portfolio()      # loads portfolio into vector DB if not already loaded
            jobs = llm.extract_jobs(data)      # extracts job details as JSON from cleaned page text
            for job in jobs:
                skills = job.get('skills', [])    # safely gets skills list (empty if missing)
                links = portfolio.query_links(skills)   # finds relevant portfolio links based on job skills
                email = llm.write_mail(job, links)      # generate personalized cold email with portfolio links
                st.code(email, language='markdown')     # display generated email in formatted code block
        except Exception as e:
            st.error(f"An Error Occurred: {e}")     # shows user-friendly error if anything breaks

if __name__ == "__main__":
    chain = Chain()     # initializing LLM chain with Groq + prompts
    portfolio = Portfolio()     # loads portfolio csv and sets up Croma vector DB
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")     # optimize UI layout + browser tab
    create_streamlit_app(chain, portfolio, clean_text)      # launches the streamlit UI