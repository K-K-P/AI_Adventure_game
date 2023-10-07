"""Module for interacting with OpenAI API
Requires langchain library"""

from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def connect_openAI(api_key, buff_memory, prompt):
    """Establish connection do OpenAI API and start the communication"""
    llm = OpenAI(openai_api_key=api_key)
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=buff_memory
    )
    return llm_chain


def create_prompt_template(template):
    """Create the template for OpenAI model.
    Template should contain all the information, features, ideas that we want the model to take into account
    when creating the game"""
    return PromptTemplate(input_variables=['chat_history', 'human_input'],
                          template=template)