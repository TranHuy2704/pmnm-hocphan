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

2. Dòng trạng thái và body kiểm thử cURL
curl -i http://127.0.0.1:8000/sv/23T1020001

Dòng trạng thái: HTTP/1.1 301 MOVED PERMANENTLY

Header quan trọng: Location: /students/23T1020001

Body:

HTML
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="/students/23T1020001">/students/23T1020001</a>. If not click the link.
curl -i http://127.0.0.1:8000/students/23T1020001/export

Dòng trạng thái: HTTP/1.1 200 OK

Header quan trọng: Content-Type: text/csv; charset=utf-8, Content-Disposition: attachment; filename=diem_23T1020001.csv

Body:

Đoạn mã
hoc_phan,diem
PMMNM,8.5
CSDL,7.0
MMT,9.0
curl -i "http://127.0.0.1:8000/api/students?lop=k47a&min_avg=7"

Dòng trạng thái: HTTP/1.1 200 OK

Header quan trọng: Content-Type: application/json

Body:

JSON
[
  {
    "average": 8.17,
    "lop": "K47A",
    "mssv": "23T1020001",
    "name": "Nguyễn Văn An",
    "rank": "Khá",
    "scores": {
      "CSDL": 7.0,
      "MMT": 9.0,
      "PMMNM": 8.5
    }
  }
]
curl -i "http://127.0.0.1:8000/api/students?min_avg=abc"

Dòng trạng thái: HTTP/1.1 400 BAD REQUEST

Header quan trọng: Content-Type: application/json

Body:

JSON
{
  "detail": "Tham số min_avg phải là số thực.",
  "error": "Dữ liệu không hợp lệ"
}
curl -i http://127.0.0.1:8000/api/students/999

Dòng trạng thái: HTTP/1.1 404 NOT FOUND

Header quan trọng: Content-Type: application/json

Body:

JSON
{
  "detail": "Không có sinh viên với MSSV = 999.",
  "error": "Không tìm thấy"
}
curl -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=9"

Dòng trạng thái: HTTP/1.1 201 CREATED

Header quan trọng: Location: /api/students/23T1020005/scores/WEB, Content-Type: application/json

Body:

JSON
{
  "average": 9.0
}
curl -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=7.5"

Dòng trạng thái: HTTP/1.1 200 OK

Header quan trọng: Content-Type: application/json

Body:

JSON
{
  "average": 7.5
}
curl -i -X PUT "http://127.0.0.1:8000/api/students/23T1020005/scores/WEB?score=11"

Dòng trạng thái: HTTP/1.1 400 BAD REQUEST

Header quan trọng: Content-Type: application/json

Body:

JSON
{
  "detail": "Điểm số phải nằm trong khoảng [0, 10].",
  "error": "Dữ liệu không hợp lệ"
}
curl -i -X DELETE http://127.0.0.1:8000/api/students/23T1020005/scores/WEB

Dòng trạng thái: HTTP/1.1 204 NO CONTENT

Body: (Rỗng)

curl -i -X POST http://127.0.0.1:8000/api/students/23T1020005/scores/WEB

Dòng trạng thái: HTTP/1.1 405 METHOD NOT ALLOWED

Header quan trọng: Content-Type: application/json

Body:

JSON
{
  "detail": "The method is not allowed for the requested URL.",
  "error": "Phương thức không được hỗ trợ"
}
curl -i -X POST http://127.0.0.1:8000/students

Dòng trạng thái: HTTP/1.1 405 METHOD NOT ALLOWED

Header quan trọng: Content-Type: text/html; charset=utf-8

Body: Trang HTML báo lỗi 405 dùng qua hàm layout().

3. Trả lời câu hỏi ngắn
Vì sao Câu 4 dùng 301 còn Câu 8 trả 201 kèm Location?

301 (Moved Permanently): Dùng để chuyển hướng vĩnh viễn đường dẫn rút gọn (/sv/<mssv>) sang URL chính thức (/students/<mssv>), giúp client/trình duyệt ghi nhớ vị trí cố định.

201 (Created): Báo hiệu rằng một tài nguyên mới (học phần điểm mới) đã được tạo thành công trên hệ thống; header Location trả về URI chính xác của tài nguyên vừa tạo theo đúng chuẩn REST.

Thêm điểm cho 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?

Không còn. Dữ liệu danh sách sinh viên hiện đang được lưu trực tiếp trên bộ nhớ RAM (biến in-memory trong Python). Khi server tắt và khởi động lại, bộ nhớ RAM bị giải phóng và ứng dụng sẽ tải lại giá trị khởi tạo gốc ban đầu trong code, do đó các thay đổi trước đó bị mất hoàn toàn.
