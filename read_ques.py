import json
import os
from datetime import datetime

# -------------------------------
# STEP 1: List available exams
# -------------------------------
EXAMS_FOLDER = "exams"

if not os.path.exists(EXAMS_FOLDER):
    print("❌ Exams folder not found.")
    exit()

exam_files = [f for f in os.listdir(EXAMS_FOLDER) if f.endswith(".json")]

if not exam_files:
    print("❌ No exam papers found.")
    exit()

print("\nAvailable Exams:")
for i, exam in enumerate(exam_files, start=1):
    print(f"{i}. {exam}")

# -------------------------------
# STEP 2: Select exam
# -------------------------------
try:
    choice = int(input("\nSelect exam number: "))
    selected_exam_file = exam_files[choice - 1]
except (ValueError, IndexError):
    print("❌ Invalid selection.")
    exit()

exam_path = os.path.join(EXAMS_FOLDER, selected_exam_file)

# -------------------------------
# STEP 3: Load selected exam
# -------------------------------
with open(exam_path, "r", encoding="utf-8") as file:
    exam_data = json.load(file)

# -------------------------------
# STEP 4: Student details
# -------------------------------
student_name = input("\nEnter your name: ")
roll_no = input("Enter your roll number: ")

# -------------------------------
# STEP 5: Start exam time
# -------------------------------
start_time = datetime.now()

# -------------------------------
# STEP 6: Display question paper
# -------------------------------
print("\n" + "-" * 40)
print("Exam ID:", exam_data["exam_id"])
print("Topic:", exam_data.get("topic", "N/A"))
print("-" * 40 + "\n")

student_answers = []

for index, question in enumerate(exam_data["questions"], start=1):
    print(f"Q{index}. {question}")
    answer = input("Your answer: ")
    student_answers.append(answer)
    print()

# -------------------------------
# STEP 7: End exam time
# -------------------------------
end_time = datetime.now()

# -------------------------------
# STEP 8: Prepare exam record
# -------------------------------
exam_record = {
    "exam_id": exam_data["exam_id"],
    "student_name": student_name,
    "roll_no": roll_no,
    "start_time": start_time.isoformat(),
    "end_time": end_time.isoformat(),
    "answers": student_answers
}

# -------------------------------
# STEP 9: Save submission safely
# -------------------------------
SUBMISSIONS_FOLDER = "submissions"
os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)

filename = f"{roll_no}_{exam_data['exam_id']}.json"
filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

if os.path.exists(filepath):
    print("❌ Exam already submitted for this roll number.")
    exit()

with open(filepath, "w", encoding="utf-8") as file:
    json.dump(exam_record, file, indent=4)

print("✅ Exam completed successfully.")
print(f"📄 Submission saved at: {filepath}")
