import json
import os
from datetime import datetime

# ---------------------------------
# Base Directory
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUBMISSIONS_FOLDER = os.path.join(BASE_DIR, "submissions")
ANSWER_KEYS_FOLDER = os.path.join(BASE_DIR, "answer_keys")
RESULT_FILE = os.path.join(BASE_DIR, "final_results.json")

# ---------------------------------
# Validate Folders
# ---------------------------------
if not os.path.exists(ANSWER_KEYS_FOLDER):
    print("❌ answer_keys folder not found.")
    exit()

if not os.path.exists(SUBMISSIONS_FOLDER):
    print("❌ submissions folder not found.")
    exit()

# ---------------------------------
# Load Answer Keys
# ---------------------------------
answer_key_files = [
    f for f in os.listdir(ANSWER_KEYS_FOLDER)
    if f.endswith(".json")
]

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

# ---------------------------------
# Evaluate Submissions
# ---------------------------------
results = []

for file_name in os.listdir(SUBMISSIONS_FOLDER):
    if not file_name.endswith(".json"):
        continue

    with open(os.path.join(SUBMISSIONS_FOLDER, file_name), "r", encoding="utf-8") as file:
        submission = json.load(file)

    if submission["exam_id"] != exam_id:
        continue

    student_answers = submission["answers"]
    score = 0

    for student_ans, correct_ans in zip(student_answers, correct_answers):
        if student_ans.strip().lower() == correct_ans.strip().lower():
            score += marks_per_question

    # Time calculation
    if "start_time" in submission and "end_time" in submission:
        start = datetime.fromisoformat(submission["start_time"])
        end = datetime.fromisoformat(submission["end_time"])
        time_taken = (end - start).seconds
    else:
        time_taken = None

    results.append({
        "roll_no": submission["roll_no"],
        "student_name": submission["student_name"],
        "score": score,
        "max_score": len(correct_answers) * marks_per_question,
        "time_taken_seconds": time_taken
    })

# ---------------------------------
# CORRECTION LOGIC
# ---------------------------------
print("\nCorrection Options:")
print("1. No correction")
print("2. Add bonus marks to all students")
print("3. Modify specific student score")

correction_choice = input("Select option: ").strip()

if correction_choice == "2":
    try:
        bonus = int(input("Enter bonus marks to add: "))
        for r in results:
            r["score"] += bonus
        print("✅ Bonus marks applied.")
    except ValueError:
        print("❌ Invalid bonus value.")

elif correction_choice == "3":
    roll = input("Enter roll number to modify: ").strip()

    for r in results:
        if r["roll_no"] == roll:
            try:
                new_score = int(input("Enter new score: "))
                r["score"] = new_score
                print("✅ Score updated.")
            except ValueError:
                print("❌ Invalid score.")
            break
    else:
        print("❌ Student not found.")

# ---------------------------------
# Save Final Results
# ---------------------------------
with open(RESULT_FILE, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)

print("\n✅ Evaluation complete.")
print(f"📊 Results saved to {RESULT_FILE}")