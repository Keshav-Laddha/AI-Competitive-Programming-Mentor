import httpx
from datetime import datetime

CODEFORCES_API="https://codeforces.com/api"

async def fetch_user_submissions(handle: str):
    url=f"{CODEFORCES_API}/user.status?handle={handle}"
    async with httpx.AsyncClient(timeout=20) as client:
        resp=await client.get(url)
        resp.raise_for_status()
        data=resp.json()

    if data["status"]!="OK":
        raise Exception("Codeforces API error")

    return data["result"]