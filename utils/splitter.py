from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_documents(text):
       text_splitter = RecursiveCharacterTextSplitter(
       # Set a really small chunk size, just to show.
       chunk_size=1024,
       chunk_overlap=100,
       length_function=len,
       is_separator_regex=False,
       separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
    ],
       )
       documents = text_splitter.create_documents([text])
       return documents