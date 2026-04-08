import numpy as np

def build_training_sample(topic_weakness: dict, problem, user_stats: dict, label: int):

    topic_features=[topic_weakness.get(tag, 0.0) for tag in problem.tags]

    avg_topic_weakness=(sum(topic_features)/len(topic_features) if topic_features else 0.0)

    # X=np.array([
    #     avg_topic_weakness,
    #     problem.difficulty or 1200,
    #     user_stats["avg_difficulty"],
    #     user_stats["attempts_on_topic"],
    #     user_stats["recent_accuracy"]
    # ], dtype=float)

    difficulty = problem.difficulty or 1200
    user_level = user_stats["avg_difficulty"]

    difficulty_gap = difficulty - user_level

    X = np.array([
        avg_topic_weakness,                 # how weak user is (for personalization)
        difficulty,                         # absolute difficulty (absolute scale)
        user_level,                         # user skill
        difficulty_gap,                     # relative difficulty (VERY IMPORTANT)
        user_stats["recent_accuracy"],      # current form (current performance)
        user_stats["attempts_on_topic"],    # activity
    ], dtype=float)

    return X, label