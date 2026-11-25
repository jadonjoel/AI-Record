# Experiment 13: Study Assistant Using Keyword Matching

import re
import sys
from pathlib import Path

import pandas as pd

default_csv = Path(__file__).with_name("experiment_13_study_materials.csv")
csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_csv
df = pd.read_csv(csv_path)

def tokenize(text):
    return set(re.findall(r"[a-zA-Z]+", str(text).lower()))

def retrieve_material(query):
    query_words = tokenize(query)
    scores = []
    for _, row in df.iterrows():
        searchable_text = " ".join([
            row["Topic"], row["Concept"], row["Explanation"], row["Keywords"]
        ])
        material_words = tokenize(searchable_text)
        score = len(query_words & material_words) / max(len(query_words), 1)
        scores.append(score)
    if not scores or max(scores) == 0:
        return None, 0
    best_index = scores.index(max(scores))
    return df.iloc[best_index], scores[best_index]

def study_assistant(query):
    material, score = retrieve_material(query)
    if material is None:
        print("No matching material found. Try another concept.")
        return
    print("\n----- PERSONALIZED STUDY NOTES -----")
    print("Topic       :", material["Topic"])
    print("Concept     :", material["Concept"])
    print("Explanation :", material["Explanation"])
    print("Match score :", round(score * 100, 2), "%")
    print("\n----- QUICK QUIZ -----")
    print("Question    :", material["Quiz_Question"])
    print("Difficulty :", material["Difficulty"])
    print("Answer      :", material["Answer"])

print("Available concepts:", ", ".join(df["Concept"].tolist()))
query = input("\nEnter a topic or concept to study: ")
study_assistant(query)
print("\nStudy assistant session completed.")
print("Matching is based on CSV keyword overlap.")
