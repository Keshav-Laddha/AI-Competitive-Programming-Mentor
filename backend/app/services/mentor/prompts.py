SYSTEM_PROMPT= """
You are a Competitive Programming Mentor.

Rules:
- Do NOT give full solutions.
- Do NOT write code.
- Give hints and conceptual guidance only.
- Explain common mistakes.
- Encourage independent thinking.
"""

def build_prompt(context: list[str], user_question: str):
    context_text = "\n".join(context)
    return f"""
{SYSTEM_PROMPT}

Context:
{context_text}

User question:
{user_question}
"""