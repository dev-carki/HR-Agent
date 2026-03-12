from backend.graph.state import GraphState
from backend.agents.parser import extract_from_pdf, parse_resume_text

def resume_parser_node(state: GraphState) -> dict:
    pdf_path = state["pdf_path"]
    
    pdf_texts, photo_path = extract_from_pdf(pdf_path=pdf_path)

    resume_data = parse_resume_text(text=pdf_texts)

    return {
          "raw_pdf_text": pdf_texts,
          "resume_data": resume_data,
          "photo_path": photo_path,
    }