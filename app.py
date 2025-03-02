import re
import base64
import streamlit as st
from ollama import chat


st.set_page_config(
    page_title="Local Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def format_reasoning_response(thinking_content):
    return (
        thinking_content.replace("<think>\n\n</think>", "")
        .replace("<think>", "")
        .replace("</think>", "")
    )


def display_message(message):
    role = "user" if message["role"] == "user" else "assistant"
    bg_color = "#000000" if role == "user" else "#E8E8E8"  
    text_align = "right" if role == "user" else "left"
    
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 10px;
            border-radius: 15px;
            margin: 5px;
            width: fit-content;
            max-width: 75%;
            text-align: {text_align};
            float: {text_align};
            clear: both;
        ">
            {message["content"]}
        </div>
        """,
        unsafe_allow_html=True
    )


def display_assistant_message(content):
    pattern = r"<think>(.*?)</think>"
    think_match = re.search(pattern, content, re.DOTALL)
    
    if think_match:
        think_content = think_match.group(0)
        response_content = content.replace(think_content, "")
        think_content = format_reasoning_response(think_content)
        
        with st.expander("💭 Thinking complete!"):
            st.markdown(think_content)
        
        display_message({"role": "assistant", "content": response_content})
    else:
        display_message({"role": "assistant", "content": content})


def display_chat_history():
    for message in st.session_state["messages"]:
        if message["role"] != "system":
            display_message(message)


def process_thinking_phase(stream):
    thinking_content = ""
    with st.status("🤔 Thinking...", expanded=True) as status:
        think_placeholder = st.empty()
        
        for chunk in stream:
            content = chunk["message"]["content"] or ""
            thinking_content += content
            
            if "<think>" in content:
                continue
            if "</think>" in content:
                content = content.replace("</think>", "")
                status.update(label="💡 Thinking complete!", state="complete", expanded=False)
                break
            think_placeholder.markdown(format_reasoning_response(thinking_content))
    
    return thinking_content


def process_response_phase(stream):
    response_placeholder = st.empty()
    response_content = ""
    
    for chunk in stream:
        content = chunk["message"]["content"] or ""
        response_content += content
        response_placeholder.markdown(response_content)
    
    return response_content


@st.cache_resource
def get_chat_model():
    return lambda messages: chat(
        model="deepseek-r1",
        messages=messages,
        stream=True,
    )


def handle_user_input():
    if user_input := st.chat_input("💬 Type your message here..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        display_message({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            chat_model = get_chat_model()
            stream = chat_model(st.session_state["messages"])
            
            thinking_content = process_thinking_phase(stream)
            response_content = process_response_phase(stream)
            
            st.session_state["messages"].append(
                {"role": "assistant", "content": thinking_content + response_content}
            )


def main():
    
    with st.sidebar:
        st.header("⚙️ Chat Settings")
        model = st.selectbox("Choose AI Model:", ["deepseek-r1", "gemini-pro", "gpt-4"])
        temperature = st.slider("Response Creativity:", 0.0, 1.0, 0.7)
        st.markdown("---")

    
    st.markdown("""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{}" width="150">
        <h1>💬 Local Chatbot</h1>
        <h4>With Thinking UI! 💡</h4>
    </div>
    """.format(base64.b64encode(open("assets/deep-seek.png", "rb").read()).decode()), unsafe_allow_html=True)

    display_chat_history()
    handle_user_input()

if __name__ == "__main__":
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    main()
