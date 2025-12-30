import numpy as np

def cosine_distance(a: np.ndarray, b: np.ndarray)->float:
    return 1-np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))

def compute_novelty(problem_embedding, recent_embeddings):
    #novelty=distance from centroid of recent problems
    if not recent_embeddings:
        return 1.0  #max novelty for cold start

    centroid=np.mean(recent_embeddings, axis=0)
    return cosine_distance(problem_embedding, centroid)