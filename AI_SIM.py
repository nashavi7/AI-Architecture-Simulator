import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import time

# ----- Configuration -----
st.set_page_config(page_title="AI System Architecture Simulator", page_icon="🧠", layout="wide")

st.title("🧠 AI System Architecture Simulator")
st.markdown("**Think like a Senior AI Architect.** Enter your project goal and get a simulated architecture proposal with estimated costs, latency, and system flow.")

# ----- Rule-Based Logic Engine -----

def classify_intent(user_input: str):
    user_input = user_input.lower()
    if any(word in user_input for word in ["support", "chatbot", "qa", "question", "document"]):
        return "RAG"
    elif any(word in user_input for word in ["analytics", "data", "report", "csv", "sql"]):
        return "Data Agent"
    elif any(word in user_input for word in ["real-time", "stream", "video", "live"]):
        return "Streaming"
    elif any(word in user_input for word in ["agent", "task", "automation", "workflow", "multi-step"]):
        return "Multi-Agent"
    else:
        return "Standard LLM"

def get_architecture_details(intent: str):
    return {
        "RAG": {
            "components": ["User Input", "Embedding Model", "Vector DB", "Retriever", "LLM", "Output"],
            "edges": [
                ("User Input", "Embedding Model"),
                ("Embedding Model", "Vector DB"),
                ("User Input", "Retriever"),
                ("Vector DB", "Retriever"),
                ("Retriever", "LLM"),
                ("LLM", "Output")
            ],
            "latency": {"Retrieval": "50-150ms", "LLM": "400-800ms"},
            "cost": "$ Low-Medium",
            "complexity": "Medium",
            "description": "Retrieval-Augmented Generation for contextual responses."
        },
        "Data Agent": {
            "components": ["User Input", "Intent Parser", "Code Generator", "Executor", "LLM", "Output"],
            "edges": [
                ("User Input", "Intent Parser"),
                ("Intent Parser", "Code Generator"),
                ("Code Generator", "Executor"),
                ("Executor", "LLM"),
                ("LLM", "Output")
            ],
            "latency": {"Total": "1.5s-5s"},
            "cost": "$$ Medium",
            "complexity": "High",
            "description": "Agent generates and executes code dynamically."
        },
        "Streaming": {
            "components": ["Stream", "Processor", "Feature Store", "Model", "Dashboard"],
            "edges": [
                ("Stream", "Processor"),
                ("Processor", "Feature Store"),
                ("Feature Store", "Model"),
                ("Model", "Dashboard")
            ],
            "latency": {"Total": "15-70ms"},
            "cost": "$$$ High",
            "complexity": "Very High",
            "description": "Real-time event-driven system."
        },
        "Multi-Agent": {
            "components": ["User", "Orchestrator", "Agent A", "Agent B", "Validator", "Output"],
            "edges": [
                ("User", "Orchestrator"),
                ("Orchestrator", "Agent A"),
                ("Orchestrator", "Agent B"),
                ("Agent A", "Validator"),
                ("Agent B", "Validator"),
                ("Validator", "Output")
            ],
            "latency": {"Total": "3-10s"},
            "cost": "$$$ Variable",
            "complexity": "Extreme",
            "description": "Multiple AI agents collaborating."
        },
        "Standard LLM": {
            "components": ["User Input", "Prompt", "LLM", "Output"],
            "edges": [
                ("User Input", "Prompt"),
                ("Prompt", "LLM"),
                ("LLM", "Output")
            ],
            "latency": {"Total": "300-800ms"},
            "cost": "$ Low",
            "complexity": "Low",
            "description": "Simple LLM API usage."
        }
    }[intent]

# ----- Plotly Graph -----

def draw_plotly_graph(components, edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=text,
        textposition="middle center",
        hoverinfo='text',
        marker=dict(size=40)
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    return fig

# ----- UI -----

st.sidebar.header("Example Inputs")
st.sidebar.markdown("- Chatbot for customer support")
st.sidebar.markdown("- Analyze CSV data automatically")
st.sidebar.markdown("- Real-time fraud detection")
st.sidebar.markdown("- Multi-agent research system")

user_goal = st.text_input("Describe your goal:")

if st.button("Simulate Architecture"):
    if not user_goal.strip():
        st.warning("Enter a use case.")
    else:
        with st.spinner("Designing system..."):
            time.sleep(1)

            intent = classify_intent(user_goal)
            details = get_architecture_details(intent)

            st.success(f"### {intent} Architecture")
            st.write(details["description"])

            col1, col2 = st.columns([2, 1])

            with col1:
                fig = draw_plotly_graph(details["components"], details["edges"])
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.write(f"**Complexity:** {details['complexity']}")
                st.write("**Latency:**")
                for k, v in details["latency"].items():
                    st.write(f"- {k}: {v}")
                st.write(f"**Cost:** {details['cost']}")