import json
import os
from datetime import datetime

SUBMISSIONS_FOLDER = "submissions"
ANSWER_KEYS_FOLDER = "answer_keys"
RESULT_FILE = "final_results.json"

# -------------------------------
# STEP 1: Select answer key
# -------------------------------
answer_key_files = [f for f in os.listdir(ANSWER_KEYS_FOLDER) if f.endswith(".json")]

if not answer_key_files:
    print("❌ No answer keys found.")
    exit()

print("\nAvailable Answer Keys:")
for i, key in enumerate(answer_key_files, start=1):
    print(f"{i}. {key}")

try:
    choice = int(input("\nSelect answer key number: "))
    selected_key_file = answer_key_files[choice - 1]
except (ValueError, IndexError):
    print("❌ Invalid selection.")
    exit()

with open(os.path.join(ANSWER_KEYS_FOLDER, selected_key_file), "r", encoding="utf-8") as file:
    answer_key = json.load(file)

correct_answers = answer_key["answers"]
marks_per_question = answer_key["marks_per_question"]
exam_id = answer_key["exam_id"]

# -------------------------------
# STEP 2: Evaluate submissions
# -------------------------------
results = []

for file_name in os.listdir(SUBMISSIONS_FOLDER):
    if not file_name.endswith(".json"):
        continue

    with open(os.path.join(SUBMISSIONS_FOLDER, file_name), "r", encoding="utf-8") as file:
        submission = json.load(file)

    if submission["exam_id"] != exam_id:
        continue  # skip other exams

    student_answers = submission["answers"]
    score = 0

    for student_ans, correct_ans in zip(student_answers, correct_answers):
        if student_ans.strip().lower() == correct_ans.strip().lower():
            score += marks_per_question

    start = datetime.fromisoformat(submission["start_time"])
    end = datetime.fromisoformat(submission["end_time"])
    time_taken = (end - start).seconds

    results.append({
        "roll_no": submission["roll_no"],
        "student_name": submission["student_name"],
        "score": score,
        "max_score": len(correct_answers) * marks_per_question,
        "time_taken_seconds": time_taken
    })

# -------------------------------
# STEP 3: Save final results
# -------------------------------
with open(RESULT_FILE, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print("\n✅ Evaluation complete.")
print(f"📊 Results saved to {RESULT_FILE}")
