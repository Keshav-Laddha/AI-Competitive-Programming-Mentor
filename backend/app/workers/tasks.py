from datetime import datetime, timezone
from uuid import UUID
from app.db.base import AsyncSessionLocal
from app.db.crud import (get_problem_by_platform_id, create_problem, create_submission)
from app.db.models import CPHandle
from app.services.codeforces import fetch_user_submissions
from app.services.analysis import get_user_weak_topics
from app.services.recommendation_engine import generate_ml_recommendations
from app.services.user_stats import get_user_stats

def sync_codeforces_handle(handle_id: UUID):
    import asyncio
    asyncio.run(_sync_codeforces_handle(handle_id))

async def _sync_codeforces_handle(handle_id: UUID):
    async with AsyncSessionLocal() as db:
        handle=await db.get(CPHandle, handle_id)
        if not handle:
            return

        submissions=await fetch_user_submissions(handle.handle)
        last_synced=handle.last_synced

        for sub in submissions:
            created_at=datetime.fromtimestamp(
                sub["creationTimeSeconds"], tz=timezone.utc
            )

            #stop once we hit already synced submissions
            if last_synced and created_at<=last_synced:
                break

            problem_data=sub["problem"]
            platform_problem_id=f"{problem_data['contestId']}-{problem_data['index']}"

            problem=await get_problem_by_platform_id(db, platform="codeforces", platform_problem_id=platform_problem_id)

            if not problem:
                problem=await create_problem(
                    db,
                    platform="codeforces",
                    platform_problem_id=platform_problem_id,
                    title=problem_data["name"],
                    tags=problem_data.get("tags", []),
                    difficulty=problem_data.get("rating")
                )

            await create_submission(
                db,
                user_id=handle.user_id,
                cp_handle_id=handle.id,
                problem_id=problem.id,
                platform_submission_id=str(sub["id"]),
                verdict=sub.get("verdict"),
                language=sub.get("programmingLanguage"),
                time_taken_ms=sub.get("timeConsumedMillis"),
                memory=sub.get("memoryConsumedBytes"),
                created_at=created_at
            )

        #update checkpoint ONCE
        handle.last_synced=datetime.now(timezone.utc)
        await db.commit()

        #trigger analytics after data is persisted
        # await get_user_weak_topics(db, handle.user_id)
        # await generate_ml_recommendations(db, handle.user_id)

        topic_weakness = await get_user_weak_topics(db, handle.user_id)

        user_stats = await get_user_stats(db, handle.user_id)

        await generate_ml_recommendations(db, handle.user_id, topic_weakness, user_stats)