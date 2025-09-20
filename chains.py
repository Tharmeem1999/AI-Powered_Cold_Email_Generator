import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()       # loads API keys from .env file

class Chain:
    def __init__(self):
        # sets up LLM with Groq API. uses Llama 3.3
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        # template to extract structured job data from scraped career page
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
        chain_extract = prompt_extract | self.llm      # chains prompt + LLM together
        res = chain_extract.invoke(input={"page_data": cleaned_text})   # runs LLM on cleaned text
        try:
            json_parser = JsonOutputParser()    # parses LLM output into JSON
            res = json_parser.parse(res.content)
        except OutputParserException:
            # handles case where LLM output is too long or malformed
            raise OutputParserException("Context too big. Unable to parse jobs.")
        # ensures return is always a list (even if one job) for consistent iteration
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        # template to generate persuasive cold email using job data + portfolio links
        prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION:
                {job_description}

                ### INSTRUCTION:
                You are Tharmeem, a business development executive at Pearl Systems. Pearl Systems is an AI & Software Consulting company dedicated to facilitating
                the seamless integration of business processes through automated tools. 
                Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
                process optimization, cost reduction, and heightened overall efficiency. 
                Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Pearl Systems 
                in fulfilling their needs.
                Also add the most relevant ones from the following links to showcase Pearl Systems's portfolio: {link_list}
                Remember you are Tharmeem, BDE at Pearl Systems. 
                Do not provide a preamble.
                ### EMAIL (NO PREAMBLE):

                """
            )
        chain_email = prompt_email | self.llm       # chains email prompt + LLM
        res = chain_email.invoke({"job_description": str(job), "link_list": links})     # generates email
        return res.content      # returns only email body

