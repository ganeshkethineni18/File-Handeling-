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

exam_files = sorted([f for f in os.listdir(EXAMS_FOLDER) if f.endswith(".json")])

if not exam_files:
    print("❌ No exam papers found.")
    exit()

# ---------------------------------
# Show Available Exams (with topic)
# ---------------------------------
print("\nAvailable Exams:")

exam_metadata = []

for i, exam_file in enumerate(exam_files, start=1):
    try:
        with open(os.path.join(EXAMS_FOLDER, exam_file), "r", encoding="utf-8") as f:
            data = json.load(f)
            topic = data.get("topic", "N/A")
            exam_metadata.append((exam_file, topic))
            print(f"{i}. {exam_file}  |  Topic: {topic}")
    except Exception:
        print(f"{i}. {exam_file}  |  (Error reading file)")

# ---------------------------------
# Select Exam
# ---------------------------------
try:
    choice = int(input("\nSelect exam number: "))
    selected_exam_file = exam_metadata[choice - 1][0]
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
# Prevent Duplicate Submission
# ---------------------------------
os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)
filename = f"{roll_no}_{exam_data['exam_id']}.json"
filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

if os.path.exists(filepath):
    print("❌ Exam already submitted for this roll number.")
    exit()

# ---------------------------------
# Start Exam
# ---------------------------------
start_time = datetime.now()

print("\n" + "=" * 50)
print(f"Exam ID: {exam_data['exam_id']}")
print(f"Topic  : {exam_data.get('topic', 'N/A')}")
print("=" * 50 + "\n")

student_answers = []

for index, q in enumerate(exam_data["questions"], start=1):
    print(f"Q{index}. {q['question']}")

    for opt_index, option in enumerate(q["options"], start=1):
        print(f"   {opt_index}. {option}")

    # Force valid input
    while True:
        try:
            choice = int(input("Select option number: "))
            if 1 <= choice <= len(q["options"]):
                selected_answer = q["options"][choice - 1]
                break
            else:
                print("⚠️ Invalid option number. Try again.")
        except ValueError:
            print("⚠️ Please enter a valid number.")

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
try:
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(exam_record, file, indent=4)
except Exception:
    print("❌ Failed to save submission.")
    exit()

print("\n✅ Exam completed successfully.")
print(f"📄 Submission saved at: {filepath}")
