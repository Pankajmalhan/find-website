import vertexai
from vertexai.language_models import TextGenerationModel
from string import Template

project_id = "accessfind-7165sxdh4e"
location = "us-central1"
model_name = "text-bison@001"

vertexai.init(project=project_id, location=location)
model = TextGenerationModel.from_pretrained(model_name)

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

       Summary:
       $ctext
       """
       prompt = Template(extract_prompt).substitute(ctext=summary)
       res= extract_keywords(prompt, 0, 1024, 0.8, 1)
       return res
