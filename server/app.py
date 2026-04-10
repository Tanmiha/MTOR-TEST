from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import glob
import uvicorn
import sys

# 1. PATH FIX: Ensure the root directory is in the system path
# This allows 'server' to find 'agents', 'utility', and 'tools'
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

# 2. IMPORT FIX
try:
    # Try importing as a sibling (standard for 'python server/app.py')
    import group_chat
    user, manager, notification_agent = group_chat.user, group_chat.manager, group_chat.notification_agent
except (ImportError, ModuleNotFoundError):
    # Try importing via the server package
    from server.group_chat import user, manager, notification_agent

app = FastAPI()

# --- SECURITY FIX ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- AUTOMATED JUDGE RESET ENDPOINT ---
@app.post("/reset")
def reset():
    try:
        if hasattr(user, 'clear_history'): user.clear_history()
        if hasattr(manager, 'clear_history'): manager.clear_history()
        if hasattr(notification_agent, 'clear_history'): notification_agent.clear_history()
        
        # Look for scripts in the root directory (one level up from /server)
        for ext in ["/*.bat", "/*.sh", "/*.txt"]:
            for filepath in glob.glob(root_path + ext):
                try: os.remove(filepath)
                except: pass
                
        return JSONResponse({"status": "reset successful"})
    except Exception as e:
        return JSONResponse({"status": "error", "details": str(e)})

# --- HUMAN UI ENDPOINTS ---
static_path = os.path.join(root_path, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def serve_ui():
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend files not found"}, status_code=404)


# --- AI COMMUNICATION ENDPOINTS ---
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_mtor(request: ChatRequest):
    # This now calls your actual agent logic
    try:
        # We use a helper to get the response from your agents
        user.initiate_chat(recipient=manager, message=request.message, clear_history=False)
        # Get the last message from the chat history
        last_msg = manager.last_message()["content"]
        return {"reply": last_msg}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}


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

# --- ENTRY POINT ---
def main():
    # Inside the container, we run from the root
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
