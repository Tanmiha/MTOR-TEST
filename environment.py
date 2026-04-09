import os
import json
import uuid
from typing import Dict, Any, Tuple
from pydantic import BaseModel

# ─── OpenEnv Typed Models ───────────────────────────────────────────────────
class EnvState(BaseModel):
    ticket_id: str
    status: str
    last_observation: str
    steps_taken: int
    reward: float
    is_done: bool

class MTORServiceEnv:
    def __init__(self):
        self.tasks = {
            "easy": "Check if the system 'spooler' service is running and report status.",
            "medium": "The user cannot find the 'MTOR_LOG' environment variable. Create it with value 'ACTIVE'.",
            "hard": "Diagnostic: The app 'AgentService' is crashing. Find the dummy log file in /data/logs/error.txt and extract the error code."
        }
        self.reset()

    def reset(self, level: str = "easy") -> str:
        """Resets the environment to a starting state."""
        self.current_ticket_id = f"TKT-{uuid.uuid4().hex[:6].upper()}"
        self.current_task = self.tasks.get(level, self.tasks["easy"])
        self.steps_taken = 0
        self.current_reward = 0.0
        self.is_done = False
        self.last_obs = f"New Ticket Assigned: {self.current_task}"
        return self.last_obs

    def step(self, action_script: str) -> Tuple[str, float, bool, Dict]:
        """
        Executes the agent's action (the generated script).
        In a real OpenEnv, this would run the code. Here, we simulate the output.
        """
        self.steps_taken += 1
        
        # --- Meaningful Reward Function Logic ---
        if not action_script or len(action_script) < 10:
            observation = "Error: Empty or invalid script submitted."
            reward = 0.0
        else:
            # Simulate progress signals
            observation = f"Script executed successfully on {self.current_ticket_id}. Logs: Service status verified."
            reward = 0.5  # Partial progress for writing a runnable script
            
            # If the script contains keywords relevant to the task
            if "status" in action_script.lower() or "os.environ" in action_script.lower():
                reward = 1.0
                self.is_done = True
        
        self.current_reward = reward
        return observation, reward, self.is_done, self.state().dict()

    def state(self) -> EnvState:
        """Returns the current state of the environment."""
        return EnvState(
            ticket_id=self.current_ticket_id,
            status="Resolved" if self.is_done else "In Progress",
            last_observation=self.last_obs,
            steps_taken=self.steps_taken,
            reward=self.current_reward,
            is_done=self.is_done
        )

# ─── Example Baseline Inference Usage ────────────────────────────────────────
if __name__ == "__main__":
    env = MTORServiceEnv()
    obs = env.reset(level="easy")
    print(f"Observation: {obs}")
    
    # Simulating an agent taking a step
    script = "import os; print(os.name)"
    new_obs, reward, done, info = env.step(script)
    print(f"Reward: {reward} | Done: {done}")