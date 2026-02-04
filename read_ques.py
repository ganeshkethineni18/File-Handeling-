import json
import os
from datetime import datetime

# ---------------------------------
# Base Directory (stable paths)
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMS_FOLDER = os.path.join(BASE_DIR, "exams")
SUBMISSIONS_FOLDER = os.path.join(BASE_DIR, "submissions")

# ---------------------------------
# Validate Exams Folder
# ---------------------------------
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

# ---------------------------------
# Select Exam
# ---------------------------------
try:
    choice = int(input("\nSelect exam number: "))
    selected_exam_file = exam_files[choice - 1]
except (ValueError, IndexError):
    print("❌ Invalid selection.")
    exit()

exam_path = os.path.join(EXAMS_FOLDER, selected_exam_file)

# ---------------------------------
# Load Exam Data
# ---------------------------------
try:
    with open(exam_path, "r", encoding="utf-8") as file:
        exam_data = json.load(file)
except Exception:
    print("❌ Failed to load exam file.")
    exit()

# ---------------------------------
# Student Details
# ---------------------------------
student_name = input("\nEnter your name: ").strip()
roll_no = input("Enter your roll number: ").strip()

if not student_name or not roll_no:
    print("❌ Name and Roll number cannot be empty.")
    exit()

# ---------------------------------
# Start Time
# ---------------------------------
start_time = datetime.now()

# ---------------------------------
# Show Questions
# ---------------------------------
print("\n" + "-" * 40)
print("Exam ID:", exam_data["exam_id"])
print("Topic:", exam_data.get("topic", "N/A"))
print("-" * 40 + "\n")

student_answers = []

for index, q in enumerate(exam_data["questions"], start=1):
    print(f"Q{index}. {q['question']}")
    
    for opt_index, option in enumerate(q["options"], start=1):
        print(f"   {opt_index}. {option}")
    
    try:
        choice = int(input("Select option number: "))
        selected_answer = q["options"][choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice. Marked as blank.")
        selected_answer = ""

    student_answers.append(selected_answer)
    print()


# ---------------------------------
# End Time
# ---------------------------------
end_time = datetime.now()

# ---------------------------------
# Prepare Submission
# ---------------------------------
exam_record = {
    "exam_id": exam_data["exam_id"],
    "student_name": student_name,
    "roll_no": roll_no,
    "start_time": start_time.isoformat(),
    "end_time": end_time.isoformat(),
    "answers": student_answers
}

# ---------------------------------
# Save Submission
# ---------------------------------
os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)

filename = f"{roll_no}_{exam_data['exam_id']}.json"
filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

if os.path.exists(filepath):
    print("❌ Exam already submitted for this roll number.")
    exit()

try:
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(exam_record, file, indent=4)
except Exception:
    print("❌ Failed to save submission.")
    exit()

print("\n✅ Exam completed successfully.")
print(f"📄 Submission saved at: {filepath}")
