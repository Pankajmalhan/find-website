import vertexai
from vertexai.language_models import TextGenerationModel
from string import Template
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import VertexAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain.output_parsers import PydanticOutputParser

class TitleKeywordsOutputParser(BaseModel):
    title: str = Field(description="title of the website")
    keywords: List[str] = Field(description="keywords of the website")


project_id = "accessfind-7165sxdh4e"
location = "us-central1"
# model_name = "text-bison@001"
MODEL_ID = "gemini-1.0-pro-002"
vertexai.init(project=project_id, location=location)
# model = TextGenerationModel.from_pretrained(model_name)
model = VertexAI(model_name=MODEL_ID)

def extract_keywords(prompt, temperature, max_decode_steps, top_k, top_p):
       response = model.predict(
              prompt,
              temperature=temperature,
              max_output_tokens=max_decode_steps,
              top_k=top_k,
              top_p=top_p,)
       return response.text

def get_keywords_and_title_from_text(summary):

       parser = PydanticOutputParser(pydantic_object=TitleKeywordsOutputParser)

       extract_prompt = """
       Given the summary of a website provided below, identify title and list the most
       relevant keywords that capture the essence and main topics of the website.
       Make concise and accurate title that reflects the main content or purpose of the website. 
       Ensure that the title is relevant and directly related to the summary provided.
       The keywords should reflect the primary subjects, services, or themes discussed
       in the summary. Focus on extracting words or short phrases that are central to
       the content, pivotal for understanding the website's purpose, and useful for
       categorizing the information. Ensure that the keywords are specific, relevant,
       and concise to provide a clear overview of the website's focus areas.

       **Format Instructions**
       {format_instructions}
       **Format Instructions**

       Summary:
       {summary}
       """
       prompt = PromptTemplate(
             template=extract_prompt, 
             input_variables=["summary"],
             partial_variables={"format_instructions": parser.get_format_instructions()}
             )
       chain = (
              {"summary": RunnablePassthrough()} 
              | prompt
              | model
              | parser
       )
       res = chain.invoke(summary)
       return res


def get_title(summary):
       extract_prompt = """
       Given the summary of a website provided below, generate a concise and accurate
       title that reflects the main content or purpose of the website. Ensure that the
       title is relevant and directly related to the summary provided. 
       The title should be succinct, ideally one line, capturing the essence of the website effectively.
       Summary:
       {summary}
       """
       prompt = PromptTemplate.from_template(extract_prompt)
       output_parser = StrOutputParser()
       chain = (
              {"summary": RunnablePassthrough()} 
              | prompt
              | model
              | output_parser
       )
       res = chain.invoke(summary)
       return res
