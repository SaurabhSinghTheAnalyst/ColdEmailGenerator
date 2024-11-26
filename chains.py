import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv


load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, name, email):
        prompt_email = PromptTemplate.from_template(
            """
            {job_description}

            ### INSTRUCTION:
            You are {name_input}, a skilled professional actively seeking opportunities to contribute to impactful projects. Tailor a cold email to the recruiter/HR regarding the job mentioned above. Your goal is to:
            1. Demonstrate genuine interest in the position and the company.
            2. Highlight your relevant skills, experiences, and achievements that align with the job description.
            3. Mention any noteworthy projects, accomplishments, or certifications that showcase your capabilities.
            4. Express enthusiasm about contributing to the company’s goals and how you can add value to their team.
            
            Also, if applicable, reference links to any portfolios, LinkedIn profiles, or projects that support your expertise: {link_list}.
            
            Remember to keep the tone professional yet approachable. Do not provide a preamble.  
            ### EMAIL (NO PREAMBLE):
            {email_input}
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links, "name_input" : str(name), "email_input" : str(email)})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))