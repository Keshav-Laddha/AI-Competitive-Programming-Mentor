import os
import redis
from rq import Queue
from rq.worker import SimpleWorker
from rq.timeouts import BaseDeathPenalty
from app.config import settings

#os.environ["RQ_WORKER_CLASS"]="rq.worker.SimpleWorker"
class NoOpDeathPenalty(BaseDeathPenalty):
    def setup_death_penalty(self): pass
    def cancel_death_penalty(self): pass

redis_conn=redis.from_url(settings.REDIS_URL)

if __name__ == "__main__":
    queue=Queue("default", connection=redis_conn)
    # worker=SimpleWorker([queue], connection=redis_conn)
    worker = SimpleWorker([queue], connection=redis_conn)
    worker.death_penalty_class = NoOpDeathPenalty
    worker.work()