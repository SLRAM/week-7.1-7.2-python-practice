# TODO: Import the necessary modules
import os
import requests
import google.generativeai as genai
from urllib.parse import urlparse
from dotenv import load_dotenv

from strings import general_context, few_shot_example_one, few_shot_example_two, topic_keywords, welcome_message, input_message, exit_message, assistant_header

def setup_api():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    
    genai.configure(api_key=api_key)
    
    model_config = {
        "temperature": 0.4,
        "top_p": 0.99,
        "top_k": 0,
        "max_output_tokens": 4096,
    }

    system_instructions = [general_context, few_shot_example_one, few_shot_example_two, topic_keywords]

    return genai.GenerativeModel('gemini-1.5-flash', generation_config=model_config, system_instruction=system_instructions)

def start_chat_with_history(model):
    history = [
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "How may I help you today?"},
    ]
    
    chat_with_history = model.start_chat(history=history)
    
    return chat_with_history

# https://ai.google.dev/gemini-api/docs/text-generation?lang=python#chat
def main():
    try:
        model = setup_api()
        chat = start_chat_with_history(model)

        print(welcome_message)

        while True:
            user_input = input(input_message).strip()

            if user_input.lower() == 'quit':
                print(assistant_header + exit_message)
                exit()

            response = chat.send_message(user_input)

            print(assistant_header + response.text)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()