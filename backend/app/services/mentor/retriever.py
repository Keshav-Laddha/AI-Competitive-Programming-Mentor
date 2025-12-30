from sqlalchemy import text

async def retrieve_context(db, query_embedding, problem_id=None, limit=5):
    sql= """select content from mentor_embeddings where (:problem_id IS NULL OR problem_id=:problem_id) order by embedding <-> :query_embedding limit :limit"""
    result=await db.execute(text(sql), {"query_embedding": query_embedding, "problem_id": problem_id, "limit": limit})
    return [row[0] for row in result.fetchall()]