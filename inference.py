import os
import sys
import re
from dotenv import load_dotenv

# Load local .env file if it exists
load_dotenv()

# --- HYBRID ENVIRONMENT VARIABLES ---
# Added AZURE_OPENAI_API_KEY as a fallback to prevent immediate crashes
API_BASE_URL = os.getenv("API_BASE_URL", os.getenv("AZURE_OPENAI_ENDPOINT", "https://mta-azoi-intelligent-ticket.openai.azure.com/"))
MODEL_NAME = os.getenv("MODEL_NAME", "mtor-gpt")
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("AZURE_OPENAI_API_KEY")

# CRITICAL FIX: Add current directory to path so 'server.group_chat' is discoverable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# REMOVED: The 'raise ValueError' that was killing the container in Phase 2

# Import agents *after* path is set
try:
    from server.group_chat import user, manager, notification_agent
except ImportError:
    # Fallback in case of different container pathing
    from group_chat import user, manager, notification_agent

def run_inference(task_prompt: str):
    """
    Executes the IT Support workflow and outputs logs in the OpenEnv format.
    """
    # [START] Requirement: Use the resolved MODEL_NAME
    print(f"[START] task=it-support env=mtor-benchmark model={MODEL_NAME}")
    
    responses = []
    rewards = []
    step_count = 0
    success = False

    original_receive = user.receive

    def receive_and_capture(*args, **kwargs):
        nonlocal step_count, success
        if len(args) >= 2:
            message = args[0]
            if isinstance(message, dict):
                content = message.get("content", "")
                
                if content and content.strip().upper() != "TERMINATE":
                    responses.append(content)
                    step_count += 1
                    
                    clean_action = content.replace('\n', ' ').replace('\r', '').replace('"', "'")
                    truncated_action = f"{clean_action[:150]}..." if len(clean_action) > 150 else clean_action
                    
                    # Check for script tags to award the reward
                    bat_match = bool(re.search(r'<\s*SCRIPT_BAT\s*>(.*?)<\s*/\s*SCRIPT_BAT\s*>', content, re.IGNORECASE))
                    sh_match = bool(re.search(r'<\s*SCRIPT_SH\s*>(.*?)<\s*/\s*SCRIPT_SH\s*>', content, re.IGNORECASE))
                    
                    if bat_match or sh_match:
                        reward = 1.00
                        is_done = "true"
                        success = True
                    else:
                        reward = 0.00
                        is_done = "false"

                    rewards.append(reward)

                    print(f"[STEP] step={step_count} action=\"{truncated_action}\" reward={reward:.2f} done={is_done} error=null")

        return original_receive(*args, **kwargs)

    user.receive = receive_and_capture

    try:
        # Check if we have what we need to start
        if not API_BASE_URL or not MODEL_NAME:
            raise ValueError("Missing essential API configuration")

        user.initiate_chat(recipient=manager, message=task_prompt)
    
    except Exception as e:
        error_msg = str(e).replace('\n', ' ')
        print(f"[STEP] step={step_count+1} action=error reward=0.00 done=true error=\"{error_msg}\"")
        rewards.append(0.00)
        success = False
        step_count += 1
    
    finally:
        user.receive = original_receive
        
        success_str = "true" if success else "false"
        rewards_str = ",".join([f"{r:.2f}" for r in rewards]) if rewards else "0.00"
        print(f"[END] success={success_str} steps={step_count} rewards={rewards_str}")


if __name__ == "__main__":
    # The judge will pass the prompt as the first argument
    test_prompt = sys.argv[1] if len(sys.argv) > 1 else "My VPN keeps disconnecting every 10 minutes."
    run_inference(test_prompt)
