from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

def embed_problem(problem) -> list[float]:
    #create semantic embedding for a problem.
    text=f"""
    Title: {problem.title}
    Tags: {', '.join(problem.tags or [])}
    """
    return model.encode(text).tolist()