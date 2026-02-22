import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents.research_agent import create_research_agent
from agents.writer_agent import create_writer_agent

load_dotenv()

app = FastAPI()

# Allow React frontend to talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DigestRequest(BaseModel):
    interests: list[str]

@app.get("/")
def root():
    return {"status": "News Digest Agent is running"}

@app.post("/generate-digest")
async def generate_digest(request: DigestRequest):
    
    async def stream_digest():
        # Step 1 — Research Agent fetches news
        research_agent = create_research_agent()
        interests_str = ", ".join(request.interests)
        
        research_result = research_agent.invoke({
            "input": f"Find the latest news articles for these topics: {interests_str}",
            "chat_history": []
        })
        
        raw_research = research_result["output"]
        
        # Step 2 — Writer Agent streams the digest
        writer_chain = create_writer_agent()
        
        async for chunk in writer_chain.astream({"research": raw_research}):
            yield chunk

    return StreamingResponse(stream_digest(), media_type="text/plain")