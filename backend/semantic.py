from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_links(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    sections = []
    for page in doc:
        for para in page.get_text().split('\n\n'):
            if len(para.split()) > 10:
                sections.append(para)
    embeddings = model.encode(sections, convert_to_tensor=True)
    links = []
    for i, section in enumerate(sections):
        scores = util.pytorch_cos_sim(embeddings[i], embeddings)[0]
        top = scores.topk(3)
        related = [sections[j] for j in top.indices if j != i]
        links.append({"section": section, "related": related})
    return links

def semantic_search(query, sections):
    q_embed = model.encode(query, convert_to_tensor=True)
    sec_embed = model.encode(sections, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(q_embed, sec_embed)[0]
    best = scores.topk(1)
    return {"section": sections[best.indices[0].item()], "score": float(best.values[0])}
def get_persona_highlights(sections, persona):
    # Example logic — customize as needed
    if persona == "student":
        return [s for s in sections if "definition" in s.lower()]
    elif persona == "researcher":
        return [s for s in sections if "study" in s.lower() or "data" in s.lower()]
    else:
        return sections
