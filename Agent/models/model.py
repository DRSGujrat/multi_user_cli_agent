from langchain_google_genai import ChatGoogleGenerativeAI
from Agent.config import api_key

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite", api_key=api_key, temperature=0
)
