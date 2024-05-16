from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from utils.llm_models import groq_model, gemini_model

llm = gemini_model()

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
       map_template = """The following is a set of documents for a website
       {docs}
       Based on this list of docs, please provide the summary about website. What actually it do, what kind of services it provide. 
       Don't create the bullet points, just proivde summary in a paragraph"""
       map_prompt = PromptTemplate.from_template(map_template)
       map_chain = LLMChain(llm=llm, prompt=map_prompt)

       # Reduce
       reduce_template = """Given the summaries below, provide a coherent paragraph summary, without any additional information or instructions:
              {docs}
              Focus on delivering the essence of the information without any formal introduction or filler text. Present the content concisely and clearly.
              Summary should contains detailed information about the website.
              Note: Maximum size of summary should be greater than 1000.
                     Give summary in form of paragraphs not as points
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

