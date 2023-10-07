"""Main file for implementing the whole logic
Provide the authentication for OpenAI API and a prompt template - it is an information for ChatGPT model.
This information will be used to give model the constraints and a set of guidelines"""

from db_interaction import connect
from db_interaction import create_history
from db_interaction import create_buff_memory
from open_ai_interaction import connect_openAI
from open_ai_interaction import create_prompt_template

ASTRA_DB_KEYSPACE: str = 'database'  # here, place the name of the keyspace given in Datastax

with open('prompt_template.txt', 'r') as template:
    prompt_template = template.read()

with open('OpenAI_key.txt', 'r') as key:
    OPENAI_API_KEY = key.read().strip()


def main():
    session = connect()
    chat_history = create_history(session, ASTRA_DB_KEYSPACE)
    chat_history.clear()
    buff_memory = create_buff_memory(chat_history)
    prompt = create_prompt_template(prompt_template)
    llm_chain = connect_openAI(OPENAI_API_KEY, buff_memory, prompt)

    choice = "Start the game"

    # Predicting:
    while True:
        response = llm_chain.predict(human_input=choice)
        print(response)
        if 'the end' in response:
            break
        choice = input('Your reply: ')

main()



