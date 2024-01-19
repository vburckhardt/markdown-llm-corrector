from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("./samples/landing-zone.md")
data = loader.load()

splitter = MarkdownHeaderTextSplitter(strip_headers=True, return_each_line=True, headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")])
split_data = splitter.split_text(data[0].page_content)

for d in split_data:
    if d.page_content not in data[0].page_content:
        print(d.page_content)
        print("------------------")

# for d in data:
#     print(d.page_content)
#     d.metadata['THIS IS CUSTOM'] = 'Hehe'
#     print(d.metadata)
#     print("####################")