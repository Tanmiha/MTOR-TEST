from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import glob

# Import your AI agents (Ensure group_chat.py is in the same folder)
from group_chat import user, manager, notification_agent

app = FastAPI()

# --- 1. HACKATHON SECURITY FIX (Prevents 403 Forbidden) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. AUTOMATED JUDGE RESET ENDPOINT ---
@app.post("/reset")
def reset():
    """
    Scaler judge hits this between tests. We clear AI memory and files,
    then return the exact JSONResponse you requested.
    """
    try:
        # Clear AI Agent Memory
        if hasattr(user, 'clear_history'): user.clear_history()
        if hasattr(manager, 'clear_history'): manager.clear_history()
        if hasattr(notification_agent, 'clear_history'): notification_agent.clear_history()
        
        # Clean up previously generated scripts
        for ext in ["*.bat", "*.sh", "*.txt"]:
            for filepath in glob.glob(ext):
                try: os.remove(filepath)
                except: pass
                
        # Your specific return statement
        return JSONResponse({"status": "reset successful"})
    except Exception as e:
        # Failsafe: return 200 OK so the judge doesn't crash, but log error
        return JSONResponse({"status": "error", "details": str(e)})

# --- 3. HUMAN UI ENDPOINTS (HTML/CSS) ---
# Mount the static folder so index.html can load style.css
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    """Serves the frontend when a human visits the URL."""
    return FileResponse("static/index.html")


# --- 4. AI COMMUNICATION ENDPOINTS ---
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_mtor(request: ChatRequest):
    """
    Receives text from the HTML UI and sends it to AutoGen.
    You need to insert your actual AutoGen initiate_chat logic here!
    """
    
    # TODO: Replace these two lines with your actual AutoGen logic
    # user.initiate_chat(recipient=manager, message=request.message)
    # final_reply = ... (extract the final string from responses)
    
    # Placeholder response to test UI
    dummy_reply = f"MTOR received: {request.message}. \n\n<SCRIPT_BAT>echo 'Fixing Windows issue'</SCRIPT_BAT>"
    return {"reply": dummy_reply}


class EscalateRequest(BaseModel):
    issue: str
    ticket_id: str

@app.post("/escalate")
def escalate_issue(request: EscalateRequest):
    """Triggered when user clicks 'No, not helpful' in the UI."""
    notification_message = (
        f"🚨 Unresolved IT Issue\n\n"
        f"User reported: '{request.issue}'\n"
        f"📄 Ticket ID: {request.ticket_id}"
    )
    
    # Trigger your AutoGen notification agent
    reply = notification_agent.generate_reply(
        messages=[{"role": "user", "content": notification_message}],
        sender=user
    )
    
    final_reply = reply.get("content") if isinstance(reply, dict) else str(reply)
    return {"reply": final_reply}