import random

def generate_question_sets(questions, num_sets=3):
    sets = []
    for _ in range(num_sets):
        q_copy = questions[:]
        random.shuffle(q_copy)
        sets.append(q_copy)
    return sets
