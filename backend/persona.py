def get_persona_highlights(sections, persona):
    keywords = {
        "student": ["definition", "example", "exercise", "summary"],
        "researcher": ["experiment", "dataset", "analysis", "methodology"],
        "analyst": ["trends", "report", "overview", "metrics"]
    }
    focus = keywords.get(persona, [])
    highlights = [s for s in sections if any(word in s.lower() for word in focus)]
    return highlights
