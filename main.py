import streamlit as st

from few_shot import FewShotPosts
from post_generator import generate_post

length_options=["Short", "Medium", "Long"]
language_options=["English", "Hinglish"]

def main():
    