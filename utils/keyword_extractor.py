import vertexai
from vertexai.language_models import TextGenerationModel
from string import Template
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import VertexAI
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field


class Person(BaseModel):
    """Information about a person."""

    # ^ Doc-string for the entity Person.
    # This doc-string is sent to the LLM as the description of the schema Person,
    # and it can help to improve extraction results.

    # Note that:
    # 1. Each field is an `optional` -- this allows the model to decline to extract it!
    # 2. Each field has a `description` -- this description is used by the LLM.
    # Having a good description can help improve extraction results.
    keywords: Optional[str] = Field(
        default=None, description="Height measured in meters"
    )
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

def get_keywords_from_text(summary):
       extract_prompt = """
       Given the summary of a website provided below, identify and list the most
       relevant keywords that capture the essence and main topics of the website.
       The keywords should reflect the primary subjects, services, or themes discussed
       in the summary. Focus on extracting words or short phrases that are central to
       the content, pivotal for understanding the website's purpose, and useful for
       categorizing the information. Ensure that the keywords are specific, relevant,
       and concise to provide a clear overview of the website's focus areas.

       **Instructions**
       Give keywords as list
       **Instructions**

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
