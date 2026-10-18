import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime
from typing import TypedDict, Annotated, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# --- 1. Relational Database Stream ---
mock_db = pd.DataFrame([
    {"order_id": "DD-101", "item": "Chicken Biryani", "status": "Delivered", "delivery_time": "15 mins ago", "customer_history": "Clean", "price": 450},
    {"order_id": "DD-102", "item": "Burger & Fries", "status": "In Kitchen", "delivery_time": "N/A", "customer_history": "Clean", "price": 250},
    {"order_id": "DD-103", "item": "Premium Sushi Platter", "status": "Delivered", "delivery_time": "5 hours ago", "customer_history": "Clean", "price": 1200},
    {"order_id": "DD-104", "item": "Pizza Margherita", "status": "Delivered", "delivery_time": "10 mins ago", "customer_history": "Flagged_For_Abuse", "price": 600}
])

def query_enterprise_records(order_id: str) -> str:
    if not order_id:
        return "None"
    return mock_db[mock_db["order_id"] == order_id.upper()].to_json(orient="records")

def find_order_by_item_keyword(text: str) -> str:
    t = text.lower()
    if "biryani" in t or "chicken" in t: return "DD-101"
    if "burger" in t or "fries" in t: return "DD-102"
    if "sushi" in t or "platter" in t: return "DD-103"
    if "pizza" in t or "margherita" in t: return "DD-104"
    return None

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    order_id: str
    behavior_category: str

# --- 2. Brain Workflows Nodes ---
def cognitive_triage_node(state: AgentState):
    st.session_state.logs.append(f"⏱️ Entering [Cognitive Triage]")
    last_msg = state["messages"][-1].content.strip()
    prompt = f'Analyze message: "{last_msg}". Classify behavior into: "bypass_or_hostile" (keys like ".", "agent"), "greeting" ("hi", "hello"), or "standard_issue". Extract order format DD-XXX. Respond strictly in JSON: {{"behavior_category": "type", "order_id": "string or null"}}'
    
    ai_analysis = st.session_state.engine_llm.invoke([HumanMessage(content=prompt)])
    try:
        data = json.loads(ai_analysis.content.strip().replace("```json", "").replace("```", ""))
    except:
        data = {"behavior_category": "standard_issue", "order_id": None}
        
    extracted_id = data.get("order_id")
    category = data.get("behavior_category")
    
    if not extracted_id and category == "standard_issue":
        extracted_id = find_order_by_item_keyword(last_msg)
        
    return {"order_id": extracted_id, "behavior_category": category, "messages": [AIMessage(content=f"Categorization: {category}")]}

def fetch_database_metrics_node(state: AgentState):
    st.session_state.logs.append(f"💾 Fetching database metrics...")
    return {"messages": [AIMessage(content=f"Data: {query_enterprise_records(state['order_id'])}")]}

def policy_and_retention_engine_node(state: AgentState):
    st.session_state.logs.append(f"🤖 Applying de-escalation engine rules...")
    history = "\n".join([m.content for m in state["messages"]])
    category = state["behavior_category"]
    
    prompt = f"""You are a skilled live chat support agent for DoorDash. History:\n{history}\nCategory: {category}\n\nSOP Rules:\n1. In Kitchen: Politely deny cancellation/refund, tell them it's being cooked fresh.\n2. Delivered & Flagged_For_Abuse: Deny refund firmly. Never use terms like 'abuse' or 'flagged'. State records verify safe delivery and apologize.\n3. Delivered & >2 hours ago: Deny refund due to expired window.\n4. Clean & recent: Approve refund dynamically.\n5. bypass_or_hostile / greeting: Do not say you are an AI. Welcome them warmly, state you have full power to fix anything right now, and ask for details.\n\nFormatting: Direct, short conversational chat response under 4 sentences. No email signatures, placeholders, or headers."""
    final_reply = st.session_state.engine_llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [final_reply]}

def evaluate_graph_routing_path(state: AgentState) -> Literal["fetch_db", "apply_policy"]:
    return "fetch_db" if state.get("order_id") else "apply_policy"

# --- 3. Build Graph State Machine ---
workflow = StateGraph(AgentState)
workflow.add_node("triage", cognitive_triage_node)
workflow.add_node("fetch_db", fetch_database_metrics_node)
workflow.add_node("apply_policy", policy_and_retention_engine_node)
workflow.add_edge(START, "triage")
workflow.add_conditional_edges("triage", evaluate_graph_routing_path, {"fetch_db": "fetch_db", "apply_policy": "apply_policy"})
workflow.add_edge("fetch_db", "apply_policy")
workflow.add_edge("apply_policy", END)
app = workflow.compile()

# --- 4. Streamlit UI Architecture ---
st.set_page_config(page_title="DoorDash Engine Suite", page_icon="🍔", layout="centered")

if "logs" not in st.session_state:
    st.session_state.logs = ["💡 Operational Core Online. Waiting for feeds..."]

if "output" not in st.session_state:
    st.session_state.output = ""

st.sidebar.title("🔑 Configuration Panel")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")

st.title("🍔 Autonomous Enterprise BPO Suite")
st.write("This application deploys a cognitive matrix designed to handle operations with 100% autonomy.")
st.dataframe(mock_db, use_container_width=True)

user_input = st.text_input("Simulate Customer Feed Message:")

# --- 5. Flat Processing Triggers (0% Indentation Nesting) ---
if st.button("Process Live Feed Transaction", type="primary"):
    if not api_key:
        st.error("Error: Please provide your API Key in the sidebar.")
    elif not user_input:
        st.warning("Warning: Message input is empty.")
    else:
        st.session_state.engine_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=api_key)
        st.session_state.logs = [f"🚀 Processing: '{user_input}'"]
        
        with st.spinner("Executing architecture channels..."):
            initial_state = {"messages": [HumanMessage(content=user_input)], "order_id": "", "behavior_category": ""}
            final_output = app.invoke(initial_state)
            st.session_state.output = final_output["messages"][-1].content

if st.session_state.output:
    st.success("🤖 Unified System Response Dispatched:")
    st.info(st.session_state.output)

st.subheader("🖥️ Real-Time Telemetry & Audit Trails")
with st.container(border=True):
    for log in st.session_state.logs:
        st.code(log, language="bash")
