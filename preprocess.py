import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
import unicodedata

def process_posts(raw_file_path, processed_file_path="data/processed_posts.json"):
    enriched_posts = []
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)

        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata # {**post , **metadata}
            enriched_posts.append(post_with_metadata)
    for epost in enriched_posts:
        