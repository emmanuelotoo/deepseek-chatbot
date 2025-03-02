#  Local Chatbot

 This Local chatbot is a Streamlit-based chatbot application that provides real-time AI responses using the Deepseek-r1 model. It features a smooth streaming UI with a unique "thinking phase" that enhances user experience.

## Features

- **Real-time AI responses** with a smooth streaming experience
- **Thinking UI** that displays the model's reasoning before providing an answer
- **Chat history** persists throughout the session
- **Efficient caching** of the chat model to reduce loading times
- **User-friendly interface** built with Streamlit

## Installation

### Prerequisites
- Python 3.8+
- Pip
- Virtual environment (optional but recommended)

### Steps


## Usage

Run the Streamlit application with:
```sh
streamlit run app.py
```

## Project Structure
```
Local-streaming-chat/
│── assets/               # Contains images like the deep-seek logo
│── app.py                # Main application file
│── requirements.txt       # Required Python packages
│── README.md             # Documentation
```

## Configuration
- **Modify AI model**: Update the `model="deepseek-r1"` in `get_chat_model()` inside `app.py` if you want to use a different model.
- **Customize UI**: Edit `st.markdown()` and `st.chat_message()` to change the chatbot’s appearance.

## Dependencies
- `streamlit`
- `ollama`
- `re`
- `base64`
