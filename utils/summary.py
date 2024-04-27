from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
from langchain_google_vertexai import VertexAI
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache

set_llm_cache(SQLiteCache(database_path=".langchain.db"))

location = "us-central1"
project_id = "accessfind-7165sxdh4e"
vertexai.init(project=project_id, location=location)

MODEL_ID="gemini-1.5-pro-preview-0409"
llm = VertexAI(model_name=MODEL_ID)

# llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

def summarize_stuff_chain(docs):
       # Define prompt
       prompt_template = """Write a concise summary of the following:
       "{text}"
       CONCISE SUMMARY:"""
       prompt = PromptTemplate.from_template(prompt_template)

       llm_chain = LLMChain(llm=llm, prompt=prompt)

       # Define StuffDocumentsChain
       stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
       return stuff_chain.run(docs)


def summarize_map_reduce(docs):
       # Map
       map_template = """The following is a set of documents
       {docs}
       Based on this list of docs, please provide the summary of text:"""
       map_prompt = PromptTemplate.from_template(map_template)
       map_chain = LLMChain(llm=llm, prompt=map_prompt)

       # Reduce
       reduce_template = """The following is set of summaries:
       {docs}
       Take these and distill it into a final, consolidated summary.
       Provide a final summary that contains the summary of list of documents. 
       Ignore the introduction text like documents provided include etc. Just give the summary
       """
       reduce_prompt = PromptTemplate.from_template(reduce_template)

       # Run chain
       reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

       # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
       combine_documents_chain = StuffDocumentsChain(
              llm_chain=reduce_chain, document_variable_name="docs"
       )

       # Combines and iteratively reduces the mapped documents
       reduce_documents_chain = ReduceDocumentsChain(
              # This is final chain that is called.
              combine_documents_chain=combine_documents_chain,
              # If documents exceed context for `StuffDocumentsChain`
              collapse_documents_chain=combine_documents_chain,
              # The maximum number of tokens to group documents into.
              token_max=4000,
       )
       # Combining documents by mapping a chain over them, then combining results
       map_reduce_chain = MapReduceDocumentsChain(
              # Map chain
              llm_chain=map_chain,
              # Reduce chain
              reduce_documents_chain=reduce_documents_chain,
              # The variable name in the llm_chain to put the documents in
              document_variable_name="docs",
              # Return the results of the map steps in the output
              return_intermediate_steps=False,
       )
       return map_reduce_chain.run(docs)

