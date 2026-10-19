# 🍔 Autonomous Enterprise BPO Suite (DoorDash CX Engine)

A production-ready, fully autonomous customer experience (CX) and support automation engine. Built using **Python**, **LangGraph**, and **OpenAI GPT-4o-mini**, hosted live via a **Streamlit** user interface.

🌐 **Live Web Application Demo:** [https://streamlit.app](https://autonomous-bpo-suite.streamlit.app/)

---

## 💡 The Business Problem & Vision
Traditional customer support platforms bleed massive amounts of money due to rigid, automated systems. Customers easily bypass standard chatbots by entering shortcut strings (like a single period `.` or the word `"agent"`), forcing expensive escalations to human specialists. 

Leveraging 21 months of real-world operational floor experience at DoorDash, I engineered a closed-loop agentic framework capable of handling complex, cyclic customer journeys with **100% full autonomy**. The engine cuts down human labor overhead and API token costs to zero while maintaining corporate compliance guardrails.

---

## ⚙️ Core System Architecture & Data Flow

The backend logic is designed as a state-driven machine modeled via a LangGraph `StateGraph`. A central, thread-safe `AgentState` object persists data natively throughout the transactional lifecycle:

1. **Cognitive Triage Node:** Analyzes user psychology and intent. It intercepts hostile punctuation/keyword spams to hold systemic authority without human takeover. If a standard complaint lacks metadata, it triggers an **Automated Semantic Lookup**—cross-referencing food item keywords (e.g., *"biryani"*) against backend database records to dynamically map the profile.
2. **Database Metrics Node:** Extracts the mapped Order ID and executes an asynchronous API-grade lookup against internal enterprise data fields to pull order metrics, timestamps, and customer history logs.
3. **Policy & Retention Engine Node:** Evaluates the internal database payload against strict Standard Operating Procedures (SOPs). It handles fraud risk indicators safely—denying claims for accounts flagged for abuse while maintaining brand diplomacy by **never accusing the customer or leaking internal security tags**.

---

## 🛠️ Tech Stack & Operational Infrastructure
* **Language:** Python 3.10+
* **State Machine Orchestration:** LangGraph (StateGraph, Conditional Edges, central AgentState management)
* **LLM Foundation Layer:** LangChain OpenAI Integration (`gpt-4o-mini` with Native Structured Tool Output schemas)
* **Frontend Design:** Streamlit Framework (Vertical data architecture, Real-time execution telemetry console)

---

## 🏃‍♂️ How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com
   cd doordash-ai-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Fire up the Streamlit server:
   ```bash
   streamlit run app.py
   ```
