# Báo cáo Bài tập Chương 3 - Sổ điểm

### 1. Kết quả routes

```text
Endpoint                   Methods    Rule
-------------------------  ---------  ------------------------------------------
api_student_course_score   DELETE,GET,PUT /api/students/<mssv>/scores/<course>
api_student_single         GET        /api/students/<mssv>
api_students               GET        /api/students
export_csv                 GET        /students/<mssv>/export
home                       GET        /
search                     GET        /search
short_student_link         GET        /sv/<mssv>
static                     GET        /static/<path:filename>
student_detail             GET        /students/<mssv>
student_list               GET        /students
