import redis
from rq import Worker, Queue
from app.config import settings

redis_conn=redis.from_url(settings.REDIS_URL)

if __name__ == "__main__":
    queue=Queue("default", connection=redis_conn)
    worker=Worker([queue], connection=redis_conn)
    worker.work()