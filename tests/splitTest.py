from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
import json
from langchain.schema import Document

def load_json_to_documents(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for item in data:
        title = item.get("title", "")
        content = item.get("content", "")
        comments = "\n".join(item.get("comments", []))
        create = item.get("create", "")

        full_text = f"{title}\n\n{content}\n\n답변:\n{comments}"
        documents.append(Document(page_content=full_text, metadata={"create": create}))
    
    return documents  
'''
text_splitter = CharacterTextSplitter(
    separator = '},\n',
    chunk_size = 900,
    chunk_overlap  = 250,
    length_function = len,
)
'''
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap  = 250,
    length_function = len,
)


data = load_json_to_documents(r'C:/Soop/연구/RagTest/ChatBotWithRag/output_data.json')
texts = text_splitter.split_documents(data)


print(len(texts))
print(texts[38])