import streamlit as st
from collections import Counter
from responses import responses, blank_spot, welcome_message
from helpers import preprocess, compare_overlap, pos_tag, extract_nouns, compute_similarity
import spacy
import en_core_web_trf
nlp = en_core_web_trf.load()
import re

st.set_page_config(page_title="🩷💬")

st.title('🩷💬')
st.title('Chat With Hourglass')

with st.sidebar:
    st.title("Exploring GenAI and Chatbots: A Series")
    st.write("This chatbot created by Tyler Shannon of Hourglass Collaborative is an ongoing exploriation and research effort into the power of Generative AI to drive better customer experiences and business outcomes.")
    st.write("You can learn more about the project here: \n\n https://hourglasscollaborative.com/")
    st.write("This chatbot is one in a series of chatbots that use different applications of AI and NLP to assist you in answering your questions.")
    st.header("🤖 Arty, the Hourglass Chatbot")
    st.write("Arty is a closed-domain retrieval-based chatbot. This means that Arty uses Natural Language Processing (NLP) to understand what you say, and then pairs the intent of your question with the best possible answer. Arty will pull the best possible answer from a document library called the \"Hourglass Knowledge Hub.\" In other words, Arty uses AI to understand you, but cannot generate unique responses all on their own.")
    st.write("To learn more about how this implemented, visit this link:\n\nhttps://hourglasscollaborative.com/")
    st.write("Though Arty cannot generate it's own responses and relies on the Knowledge Hub, other chatbots in this series will be able to do that. We'll be using Retrieval-Augmented and Generative Models later on, so stay tuned.")
    st.write("NOTE: Your responses and data provided as prompt inputs are not saved to any external databases. Your chat history will be chached in your browser and will only be accessible to you, and you alone.")

avatars = {"user":"💻", "assistant":"🤖"}

exit_commands = ("goodbye", "good bye", "exit", "stop", "cya", "talk later", "done", "that's enough")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": welcome_message}]


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = avatars[message["role"]]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt_input):
    for command in exit_commands:
        if command in prompt_input:
            st.write("Goodbye")
            return ""
    best_response = find_intent_match(prompt_input, responses)
    return best_response

# Function for defining the intent
def find_intent_match(prompt_input, responses):
    # print(f'Prompt Input: {prompt_input}')
    bow_prompt = Counter(preprocess(prompt_input))
    # print(f'Prompt BOW: {bow_prompt}')
    processed_responses = [Counter(preprocess(response)) for response in responses]

    similarity_list = [compare_overlap(response, bow_prompt) for response in processed_responses]
    # print(f'Similarity List: {similarity_list}')
    response_index = similarity_list.index(max(similarity_list))
    # print(f'Response Index: {response_index}')

    return responses[response_index]

# Funtion for removing tags from reponses
def remove_tags(text):
    pattern = re.compile(r'\#\w+')
    
    # re.sub() function replaces the pattern with an empty string.
    cleaned_text = re.sub(pattern, '', text)
    
    return cleaned_text

# User-provided prompt
if prompt := st.chat_input("Type your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar = avatars["user"]):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar = avatars["assistant"]):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            cleaned_response = remove_tags(response)
            st.write(cleaned_response)
    message = {"role": "assistant", "content": cleaned_response}
    st.session_state.messages.append(message)
