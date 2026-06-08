# Belajar lebih banyak tentang FASTAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
# Bikin servis API
app = FastAPI(title="Simple LLM API", version="1.0.0")
class ChatRequest(BaseModel):
    question:str
    history:str = ""

class ChatResponse(BaseModel):
    answer: str
    token_input: int
    token_output: int

def build_chain():
    llm = ChatOpenAI(model="gpt-4o-mini",
                     api_key = os.getenv("OPENAI_API_KEY"),)
    prompt = ChatPromptTemplate.from_messages([("system", (f'''You are a helpful assistant.
                                                           Use the conversation history below to provide context-aware responses.
                                                           Conversation History: {history}'''),),
                                                ("human", "{question}"),])
    return prompt | llm

chain = build_chain()

#.post = POST bukan GET
@app.post("/chat", response_model=ChatResponse)

#async = ga perlu nunggu fungsi ini selesai(orang pertama dulu harus selesai baru orang kedua jalan itu ga perlu)
##
async def chat(request: ChatRequest):
    try:
        response = chain.invoke({"question": request.question,
                                 "history": request.history,})
        usage = response.usage_metadata
        return ChatResponse(answer = response.content,
                            token_input = usage["input_tokens"],
                            token_output= usage["output_tokens"],)
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

#cek aplikasinya jalan (up) atau nga
@app.get("/health")
async def health():
    return {"status": "ok"}