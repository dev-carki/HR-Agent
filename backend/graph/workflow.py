from langgraph.graph import StateGraph, START, END

from backend.graph.state import GraphState
from backend.graph.nodes import (
    resume_parser_node, 
    photo_analyze_node,
    aggregator_node,
    career_analyze_node,
    personal_info_analyze_node,
    self_intro_analyze_node,
    skill_match_analyze_node
)

def build_graph():
    builder = StateGraph(GraphState)
    
    # 노드 추가
    builder.add_node("resume_parser", resume_parser_node)
    builder.add_node("photo_analyze_agent", photo_analyze_node)
    builder.add_node("personal_info_analyze_agent", personal_info_analyze_node)
    builder.add_node("skill_match_analyze_agent", skill_match_analyze_node)
    builder.add_node("self_intro_analyze_agent", self_intro_analyze_node)
    builder.add_node("career_analyze_agent", career_analyze_node)
    builder.add_node("aggregator", aggregator_node)
    
    # 엣지
    builder.add_edge(START, "resume_parser")
    
    builder.add_edge("resume_parser", "photo_analyze_agent")
    builder.add_edge("resume_parser", "personal_info_analyze_agent")
    builder.add_edge("resume_parser", "skill_match_analyze_agent")
    builder.add_edge("resume_parser", "self_intro_analyze_agent")
    builder.add_edge("resume_parser", "career_analyze_agent")
    
    builder.add_edge("photo_analyze_agent", "aggregator")
    builder.add_edge("personal_info_analyze_agent", "aggregator")
    builder.add_edge("skill_match_analyze_agent", "aggregator")
    builder.add_edge("self_intro_analyze_agent", "aggregator")
    builder.add_edge("career_analyze_agent", "aggregator")
    
    builder.add_edge("aggregator", END)
    
    return builder.compile()