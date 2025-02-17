import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key = os.getenv("groq_api_key"))

    def extract_jobs(self, cleaned_text):
        extract_prompt = PromptTemplate.from_template(
            """
            This is data from the company's website :
            {page_content}

            Now, use this data to extract relevent job description, role and skills in JSON format.
            Don't give anything else but the JSON output with the following keys : 'role', 'description', 'skills'
            """
        )

        chain_extract = extract_prompt | self.llm
        res = chain_extract.invoke(input={'page_content': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            Job Description:
            {job_description}

            ### Instructions:
            You are Dhruvil Joshi, a Data Science graduate student from Indiana University at Bloomington. You have also done your undergraduate in Artificial Intelligence and Data Science.
            So you have the right foundations in the field of Data Science, Machine learning, deep learning and related.
            Currently you are looking for Summer Internship roles, so that you can convert your theoritical knowledge into solving real world problems.
            You are self motivated, fast learner and looking forward to spent time with smart peer group during this summer in this internship.

            write a cold email to the hiring manager regarding the job mentioned above describing the qualities and introduction mentioned above.
            Also add the most relevant ones from the following links to showcase your skills: {link_list}.
            keep the email not too long.

            Remember you are Dhruvil Joshi, a Data Science graduate student.
            No preamble
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": job, "link_list": links})
        return res.content
    
if __name__ == "__main__":
    print(os.getenv("groq_api_key"))