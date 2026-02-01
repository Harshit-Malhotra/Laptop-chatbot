import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# ADK imports
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Initialize app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "user_default"
    session_id: str = "session_default"

# ADK Runner will be lazy loaded to allow checking env vars first
runner = None
session_service = InMemorySessionService()

@app.on_event("startup")
async def startup_event():
    global runner
    try:
        from agent import root_agent
        # Check if API Key is set
        if not os.getenv("GOOGLE_API_KEY") or "Insert-Key-Here" in os.getenv("GOOGLE_API_KEY", ""):
            print("WARNING: GOOGLE_API_KEY is not set or invalid.")
        
        runner = Runner(agent=root_agent, session_service=session_service, app_name="laptop_advisor", auto_create_session=True)
    except Exception as e:
        print(f"Failed to initialize runner: {e}")

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    global runner
    if not runner:
        return {"response": "System Error: The AI agent failed to initialize. Please check the server logs (likely missing API Key)."}

    try:
        # Create user message content
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )

        response_text = ""
        
        # Run agent
        events = runner.run(
            user_id=request.user_id,
            session_id=request.session_id,
            new_message=new_message
        )

        for event in events:
            print(f"DEBUG EVENT: {event}") # Debug log
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text

        if not response_text:
             return {"response": "System Error: No response text received from the agent. Please check if your API Key is valid and has quota."}

        return {"response": response_text}
    except ValueError as ve:
        # Catch specific ADK missing key error message if possible, or general ValueError
        if "Missing key inputs argument" in str(ve):
             return {"response": "Configuration Error: Missing GOOGLE_API_KEY. Please add your API key to the .env file."}
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(ve)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv() # Load .env file
    uvicorn.run(app, host="0.0.0.0", port=8000)
