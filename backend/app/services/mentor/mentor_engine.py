from app.services.mentor.embeddings import embed_text
from app.services.mentor.retriever import retrieve_context
from app.services.mentor.prompts import build_prompt
from app.services.mentor.llm_client import call_llm

async def mentor_reply(db, user_question: str, problem_id=None):
    query_embedding=embed_text(user_question)

    context=await retrieve_context(db, query_embedding, problem_id=problem_id)

    prompt=build_prompt(context, user_question)

    return call_llm(prompt)