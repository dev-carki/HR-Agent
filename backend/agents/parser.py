from pathlib import Path

import fitz
from PIL import Image

from backend.llm.openai import OpenAILLM
from backend.models.graph_types import ResumeData
from backend.prompts.parser import PARSER_SYSTEM_PROMPT

# (텍스트, 사진경로)
def extract_from_pdf(pdf_path: str | Path, image_dir: str = "uploads") -> tuple[str, str | None]:
    pdf_name = Path(pdf_path).stem
    img_dir = Path(image_dir)
    img_dir.mkdir(exist_ok=True)
    doc = fitz.open(pdf_path)
    
    text_parts: list[str] = []
    photo_path = None
    
    for page_no in range(doc.page_count):
        page = doc.load_page(page_no)
        blocks = page.get_text("dict")["blocks"]
        
        image_index = 0
        
        for block in blocks:
            bbox = tuple(block["bbox"])
            
            # TEXT
            if block["type"] == 0:
                text = "".join(
                    span["text"]
                    for line in block["lines"]
                    for span in line["spans"]
                ).strip()
                
                text_parts.append(text)
                
            # IMAGE
            elif block["type"] == 1:
                image_index += 1
                clip = fitz.Rect(bbox)
                pix = page.get_pixmap(clip=clip, dpi=300)

                image_id = f"{pdf_name}_{page_no+1}_{image_index}"
                applicant_image_dir = img_dir / pdf_name
                applicant_image_dir.mkdir(exist_ok=True)
                applicant_image_path = applicant_image_dir / f"{image_id}.png"
                pix.save(applicant_image_path)

                img = Image.open(applicant_image_path)
                img.thumbnail((512, 512))
                img.save(applicant_image_path, "PNG", optimize=True)

                if photo_path is None:
                    photo_path = str(applicant_image_path)
    
    return "\n".join(text_parts), photo_path

# (LLM 호출)
def parse_resume_text(text: str) -> ResumeData:
    llm = OpenAILLM()

    result = llm.chat_json(content=text, system_prompt=PARSER_SYSTEM_PROMPT)
    
    return ResumeData(**result)