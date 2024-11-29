import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Code Sathi", page_icon="🧑‍💻", layout="wide")

key = st.secrets["keys"]["private"]
genai.configure(api_key=key)
model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro-latest", 
    system_instruction="""
        1. Code Analysis: Identify bugs, errors, inefficiencies, and areas of improvement in submitted code snippets.
        2. Feedback: Provide a concise summary of the issues found and actionable suggestions to fix them.
        3. Solution: Deliver optimized and corrected code snippets adhering to best practices.
        4. Clarity: Use clear, concise, and professional language while ensuring solutions are easy to understand.
        5. User Info Disclosure: Only reveal information about Unique Adhikari, who is student and currently learning AI/ML, also worked on many previous projects like movie recommendation, info hunt, news detection, diabetes prediction, stock prediction and many more web development as a backend and sometimes fullstack. if the user explicitly asks.
    """
)
chatbot = model.start_chat(history=[])

st.markdown("""
    <style>
    .stChatMessage { margin-bottom: 15px; padding: 10px; border-radius: 10px; }
    .stChatMessage.human { background-color: #e6f2ff; border-left: 4px solid #3182ce; }
    .stChatMessage.assistant { background-color: #f0f9ff; border-left: 4px solid #4299e1; }
    .stTitle { color: #2c3e50; text-align: center; margin-bottom: 20px; }
    .stTextInput > div > div > input { border: 2px solid #3182ce; border-radius: 10px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("images/codesathi.png", width=250)
    st.markdown("## About Code Sathi")
    st.markdown("""
        Code Sathi is an AI-powered code analysis tool that helps developers:
        - Identify bugs and errors
        - Optimize code efficiency
        - Provide actionable improvements
        - Learn best coding practices
    """)
    st.markdown("### Supported Languages")
    st.markdown("- Python\n- JavaScript\n- Java\n- C++\n- And more!")

st.markdown("<h1 class='stTitle'>🤖 <span style='color:#e74c3c;'>Code</span> <span style='color:#3498db;'>Sathi</span></h1>", unsafe_allow_html=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"role": "ai", "text": "This is a specialized Generative AI application designed to analyze code, identify errors and bugs, and provide optimized suggestions to enhance its quality and functionality."}
    ]

for message in st.session_state.conversation:
    role = "human" if message["role"] == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(message["text"])

human_prompt = st.chat_input("Enter your code snippet or programming question")

if human_prompt:
    st.session_state.conversation.append({"role": "human", "text": human_prompt})
    with st.chat_message("human"):
        st.markdown(human_prompt)
    with st.spinner('Analyzing code...'):
        response = chatbot.send_message(human_prompt)
        st.session_state.conversation.append({"role": "ai", "text": response.text})
        with st.chat_message("assistant"):
            st.markdown(response.text)
