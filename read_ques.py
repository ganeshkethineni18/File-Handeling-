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

exam_files = sorted([
    f for f in os.listdir(EXAMS_FOLDER)
    if f.endswith(".json")
])

if not exam_files:
    print("❌ No exam papers found.")
    exit()

# ---------------------------------
# Load Exam Metadata Safely
# ---------------------------------
print("\nAvailable Exams:")

exam_metadata = []

for exam_file in exam_files:
    full_path = os.path.join(EXAMS_FOLDER, exam_file)

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            exam_id = data.get("exam_id", "UNKNOWN")
            topic = data.get("topic", "N/A")

            exam_metadata.append({
                "file": exam_file,
                "exam_id": exam_id,
                "topic": topic
            })

    except Exception:
        print(f"⚠️ Skipping corrupted exam file: {exam_file}")

# Check again after filtering corrupted files
if not exam_metadata:
    print("❌ No valid exam files available.")
    exit()

# Display valid exams
for i, exam in enumerate(exam_metadata, start=1):
    print(f"{i}. {exam['file']}  |  Topic: {exam['topic']}")

# ---------------------------------
# Select Exam
# ---------------------------------
try:
    choice = int(input("\nSelect exam number: ").strip())

    if choice < 1 or choice > len(exam_metadata):
        raise ValueError

    selected_exam = exam_metadata[choice - 1]
    selected_exam_file = selected_exam["file"]

except ValueError:
    print("❌ Invalid selection.")
    exit()

exam_path = os.path.join(EXAMS_FOLDER, selected_exam_file)

# ---------------------------------
# Load Full Exam Data
# ---------------------------------
try:
    with open(exam_path, "r", encoding="utf-8") as file:
        exam_data = json.load(file)

    if "questions" not in exam_data:
        print("❌ Invalid exam format (missing questions).")
        exit()

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

filename = f"{roll_no}_{exam_data.get('exam_id', 'UNKNOWN')}.json"
filepath = os.path.join(SUBMISSIONS_FOLDER, filename)

if os.path.exists(filepath):
    print("❌ Exam already submitted for this roll number.")
    exit()

# ---------------------------------
# Start Exam
# ---------------------------------
start_time = datetime.now()

print("\n" + "=" * 50)
print(f"Exam ID: {exam_data.get('exam_id', 'UNKNOWN')}")
print(f"Topic  : {exam_data.get('topic', 'N/A')}")
print("=" * 50 + "\n")

student_answers = []

# ---------------------------------
# Question Loop
# ---------------------------------
for index, q in enumerate(exam_data["questions"], start=1):

    question_text = q.get("question", "Invalid question")
    options = q.get("options", [])

    if not options:
        print(f"⚠️ Question {index} has no options. Skipping.")
        student_answers.append("")
        continue

    print(f"Q{index}. {question_text}")

    for opt_index, option in enumerate(options, start=1):
        print(f"   {opt_index}. {option}")

    # Force valid selection
    while True:
        try:
            choice = int(input("Select option number: ").strip())

            if 1 <= choice <= len(options):
                selected_answer = options[choice - 1]
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
# Prepare Submission Record
# ---------------------------------
exam_record = {
    "exam_id": exam_data.get("exam_id", "UNKNOWN"),
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

# ---------------------------------
# Success Message
# ---------------------------------
print("\n✅ Exam completed successfully.")
print(f"📄 Submission saved at: {filepath}")
