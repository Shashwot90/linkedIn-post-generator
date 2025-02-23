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
        print(epost)

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags'] = list(new_tags)

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def clean_text(text):
    # Explicitly replace problematic surrogates
    text = text.replace('\ud83e', ' ')
    # Normalize text to NFC form (Standard Unicode)
    text = unicodedata.normalize('NFC', text)
    # Remove unencodable surrogates
    text = text.encode('utf-8', errors='surrogatepass').decode('utf-8', errors='ignore')
    return text

def extract_metadata(post):
    # return {
    #     'line': 10,
    #     'langiage': 'Eng'
    # }
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)

    Here is the actual post on which you need to perform this task:
    