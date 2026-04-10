from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import glob
import uvicorn
import sys

# Ensure the root directory is in the path so it can find group_chat.py
# if it's still in the root folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your AI agents
try:
    from server.group_chat import user, manager, notification_agent
except ImportError:
    # Fallback if group_chat is moved inside the server folder
    from .group_chat import user, manager, notification_agent

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
    Scaler judge hits this between tests. We clear AI memory and files.
    """
    try:
        # Clear AI Agent Memory
        if hasattr(user, 'clear_history'): user.clear_history()
        if hasattr(manager, 'clear_history'): manager.clear_history()
        if hasattr(notification_agent, 'clear_history'): notification_agent.clear_history()
        
        # Clean up previously generated scripts
        # Adjust path to look in the parent directory since we are now in /server
        for ext in ["../*.bat", "../*.sh", "../*.txt"]:
            for filepath in glob.glob(ext):
                try: os.remove(filepath)
                except: pass
                
        return JSONResponse({"status": "reset successful"})
    except Exception as e:
        return JSONResponse({"status": "error", "details": str(e)})

# --- 3. HUMAN UI ENDPOINTS (HTML/CSS) ---
# Assuming 'static' folder remains at the root
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def serve_ui():
    """Serves the frontend when a human visits the URL."""
    index_path = os.path.join(static_path, "index.html")
    return FileResponse(index_path)


# --- 4. AI COMMUNICATION ENDPOINTS ---
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_mtor(request: ChatRequest):
    # Placeholder response to test UI
    dummy_reply = f"MTOR received: {request.message}. \n\n<SCRIPT_BAT>echo 'Fixing Windows issue'</SCRIPT_BAT>"
    return {"reply": dummy_reply}


class EscalateRequest(BaseModel):
    issue: str
    ticket_id: str

@app.post("/escalate")
def escalate_issue(request: EscalateRequest):
    notification_message = (
        f"🚨 Unresolved IT Issue\n\n"
        f"User reported: '{request.issue}'\n"
        f"📄 Ticket ID: {request.ticket_id}"
    )
    
    reply = notification_agent.generate_reply(
        messages=[{"role": "user", "content": notification_message}],
        sender=user
    )
    
    final_reply = reply.get("content") if isinstance(reply, dict) else str(reply)
    return {"reply": final_reply}

# --- 5. ENTRY POINT FOR OPENENV ---
def main():
    """
    This function is what [project.scripts] server = "server.app:main" calls.
    """
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()