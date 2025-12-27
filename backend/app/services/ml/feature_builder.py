import numpy as np

def build_topic_features(topic_stats: dict): #converts weak topic stats into ML feature vectors

    features={}

    for topic, stats in topic_stats.items():
        vector=np.array([
            stats["attempts"],
            stats["solved"],
            stats["accuracy"],
            stats["avg_difficulty"],
            stats["weakness_score"]
        ], dtype=float)

        features[topic]=vector

    return features