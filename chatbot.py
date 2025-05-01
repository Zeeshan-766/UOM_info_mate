import streamlit as st
import base64
from streamlit_chat import message

# Import the ChatBot class
from chatbot_backend import ChatBot

# Initialize ChatBot instance
cohere_api_key = 'your_api_key'

chat_bot = ChatBot(cohere_api_key)

# Define a CSS style for the avatar
user_avatar_style = """
    background-color: #ffbd33;
    color: green;
    padding: 10px;
    width: 50px;
    height: 20px;
    text-align: center;
    font-weight: bold;
    font-size: 15px;
    border-radius: 40px;
    display: flex;
    justify-content: center;
    align-items: center; 
    font-family: 'Roboto', sans-serif;
    border: 1px solid #000;
"""

bot_avatar_style = """
    background-color: #008000;
    color: yellow;
    padding: 10px;
    width: 50px;
    height: 20px;
    text-align: center;
    font-weight: bold;
    font-size: 15px;
    border-radius: 50px;
    display: flex;
    justify-content: center; 
    align-items: center; 
    font-family: 'Roboto', sans-serif; 
    border: 1px solid #000;
"""

# CSS style for the p tag
paragraph_id = '''
    font-family: 'Roboto', sans-serif;
    line-height: 1.5;
    animation: fadeIn 2s ease-in-out;
    color: green;

'''
# Load the image and encode it to base64
image_path = r"C:\Users\DELL\Downloads\UOMlogo.png"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Display the image with circular CSS
st.markdown(
   f"""
    <style>
    .centered-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        */flex-direction: column;*/
        */margin-top: 5px;*/
        height: 400px;  /* Adjust height as needed */
    }}
    .circular-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
    }}
    </style>
    <div class="centered-container">
        <img src="data:image/jpg;base64,{encoded_image}" class="circular-img">
    </div>
    """,
    unsafe_allow_html=True
)


# Function to display messages
def display_message(text, is_user=False, key=None):
    if is_user:
        st.write(f'<div style="{user_avatar_style}">User</div> {text}', unsafe_allow_html=True)
    else:
        st.write(f'<div style="{bot_avatar_style}">Bot</div> {text}', unsafe_allow_html=True)

# Streamlit app
st.title("Chat With University Bot")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []




# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("User:",placeholder="Type your message here...", key="input")
    return input_text

user_input = get_text()

if user_input:
    # Get relevant documents and generate response
    relevant_documents = chat_bot.query_documents(user_input)
    response = chat_bot.generate_response_with_context(user_input, relevant_documents)
    
    # Store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        display_message(st.session_state['generated'][i])
        display_message(st.session_state['past'][i], is_user=True)
