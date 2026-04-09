---
title: MTOR Intelligent IT Resolver
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 8501
tags:
  - openenv
  - multi-agent
  - it-support
---

# 🚀 MTOR – Intelligent, Script-Driven Support

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![OpenAI](https://img.shields.io/badge/LLM-OpenAI-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

> **MTOR (Multi-agent Ticket Orchestrator & Resolver)** is an AI-powered system that automates IT ticket resolution using intelligent agents, structured knowledge, and tool-driven workflows.

---

# 🌍 Environment Overview & Motivation

Traditional IT support systems are:
- Slow ⏳  
- Manual 👨‍💻  
- Repetitive 🔁  

MTOR introduces a **multi-agent AI environment** where:
- Agents collaborate to resolve tickets  
- Knowledge is reused via structured storage  
- Actions like notifications are automated  

### 🎯 Motivation

- Reduce IT workload  
- Improve response time  
- Automate repetitive troubleshooting  
- Build scalable AI support systems  

---

# 🧠 System Architecture

MTOR follows a **multi-agent pipeline**:

1. **Classifier Agent** → Categorizes the issue  
2. **Knowledge Base Agent** → Retrieves solution  
3. **Notification Agent** → Sends response  

---

## 🏗️ Architecture Diagram

```mermaid
flowchart TD

User[👤 User Ticket] --> A[Classifier Agent]
A -->|Category| B[Knowledge Base Agent]
B -->|Solution| C[Notification Agent]
C -->|Response| User

B --> KB[(Knowledge Base JSON)]
B --> Tool1[KB Tool]

C --> Tool2[Email Tool]

subgraph MTOR System
A
B
C
end

🔄 Environment Design
📥 Observation Space

Represents what each agent receives:

User ticket (text)
Conversation history
Ticket category
Retrieved knowledge

Example:
{
  "ticket": "my wifi is not connecting",
  "history": [],
  "category": "Network Issue"
}

⚙️ Action Space

Defines what agents can do:

Agent	              Actions
ClassifierAgent	    Assign category
KnowledgeBaseAgent	Retrieve solution
NotificationAgent	  Send email

Example:
{
  "action": "retrieve_solution",
  "query": "wifi not connecting"
}

🧪 Task Descriptions & Difficulty
Task	                  Description	            Difficulty
Ticket Classification	  Categorize issue	      🟢 Easy
Knowledge Retrieval	    Fetch solution	        🟡 Medium
Agent Coordination	    Multi-agent flow	      🟡 Medium
Notification	          Send response	          🟢 Easy
End-to-End Resolution	  Full automation	        🔴 Hard

📁 Project Structure
MTOR-Intelligent-Script-Driven-Support/
│
├── agents/
│   ├── classifier_agent.py
│   ├── knowledge_base_agent.py
│   └── notification_agent.py
│
├── data/
│   └── knowledge_base.json
│
├── tools/
│   ├── knowledge_base_tool.py
│   └── send_email.py
│
├── utility/
│   ├── llm_config.py
│   └── prompt.py
│
├── app.py
├── group_chat.py
├── agent_test.py
├── create_and_upload_index.py
├── environment.py
├── Dockerfile
├── openenv.yaml
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/tanmiha/mtor-support-system.git
cd MTOR-Intelligent-Script-Driven-Support

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create .env file:
OPENAI_API_KEY=your_api_key
EMAIL_USER=your_email
EMAIL_PASSWORD=your_password

▶️ Usage
Run Full System
python app.py

Test Agents
python agent_test.py

Build Knowledge Index
python create_and_upload_index.py

🐳 Docker Usage
Build Image
docker build -t mtor-app .

Run Container
docker run -it --rm -p 8501:8501 --env-file .env mtor-app

🎥 Demo
Input Ticket:

"My WiFi is not connecting"

System Output:

Classified as: Network Issue
Retrieved solution from KB
Notification sent to user

📊 Baseline Performance
Component	                Metric	              Score
Classification Accuracy	  Category prediction	  ~85–90%
Knowledge Retrieval	      Relevant match	      ~80%
End-to-End Resolution	    Fully resolved	      ~70–75%
Response Time	            Avg latency	          < 3 sec

⚠️ Depends on prompt quality and knowledge base coverage.

📖 Research Perspective

MTOR can be modeled as a multi-agent intelligent system:

🧠 Formalization
State (S):
Ticket + history + retrieved context
Action (A):
Classification, retrieval, notification
Transition (T):
Agent-to-agent communication
Reward (R):
+1 → Correct resolution
0 → Partial
-1 → Incorrect

🔬 Research Extensions
Multi-agent coordination optimization
Tool-augmented reasoning
RL-based agent improvement
Autonomous IT benchmarking

🔧 Configuration
LLM Setup
utility/llm_config.py

Prompt Engineering
utility/prompt.py

🚀 Future Improvements
🔍 Vector DB (FAISS / Pinecone)
📊 Dashboard analytics
🌐 Web UI
🔁 Learning feedback loop
🧠 Memory-enabled agents

🏆 Hackathon Highlights
⚡ Built a multi-agent AI system for IT automation
🤖 Integrated LLMs with tool-based execution
📚 Designed a reusable knowledge base system
🐳 Fully containerized with Docker
⏱️ Real-time ticket resolution pipeline

📄 License
MIT License

💡 Tagline
MTOR – Automating IT Support with Intelligent Multi-Agent Systems