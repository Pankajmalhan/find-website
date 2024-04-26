from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

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

