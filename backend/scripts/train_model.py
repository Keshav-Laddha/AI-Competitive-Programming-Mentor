# scripts/train_model.py

import asyncio
from app.services.ml.train_model import train_solve_probability_model

async def main():
    result = await train_solve_probability_model({}, {})
    print(result)

asyncio.run(main())