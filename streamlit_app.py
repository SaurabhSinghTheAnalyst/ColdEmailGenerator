import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

class streamlit_app: 


    def create_streamlit_app(llm, portfolio, clean_text): 
        st.title("📧 Cold Email Generator")

        col1, col2 = st.columns(2)

        with col1:
            url_input = st.text_input("Enter a URL:")
            name_input = st.text_input("Enter your name")
            email_input = st.text_input("Enter your email")
            submit_button = st.button("Submit")


        if submit_button:
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                for job in jobs: 
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    name = name_input
                    email_input = email_input
                    email = llm.write_mail(job, links, name, email_input)
                    with col2:
                        st.code(email, language='markdown')
            except Exception as e:
                st.error(f"An error occured {e}")
            




