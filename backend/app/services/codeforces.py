import httpx
from datetime import datetime

CODEFORCES_API="https://codeforces.com/api"

class CodeforcesError(Exception):
    pass

async def fetch_user_submissions(handle: str, limit: int=500):
    url=f"{CODEFORCES_API}/user.status"
    params={
        "handle": handle,
        "count": limit
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp=await client.get(url, params=params)
    
    if resp.status_code != 200:
        raise CodeforcesError("Failed to reach Codeforces API")

    data=resp.json()

    if data["status"]!="OK":
        raise Exception("Codeforces API error")

    return data["result"]