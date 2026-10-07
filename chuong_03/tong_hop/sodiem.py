import csv
import io
from markupsafe import escape
from flask import Flask, request, jsonify, url_for, redirect, abort, make_response

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A",
                   "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A",
                   "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B",
                   "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B",
                   "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A",
                   "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C",
                   "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

def average(scores):
    if not scores:
        return None
    vals = list(scores.values())
    return round(sum(vals) / len(vals), 2)

def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    if avg >= 8.5:
        return "Giỏi"
    if avg >= 7.0:
        return "Khá"
    if avg >= 5.0:
        return "Trung bình"
    return "Yếu"

def student_summary(mssv):
    std = STUDENTS.get(mssv)
    if not std:
        return None
    avg = average(std["scores"])
    return {
        "mssv": mssv,
        "name": std["name"],
        "lop": std["lop"],
        "scores": std["scores"],
        "average": avg,
        "rank": rank(avg)
    }

def layout(title, body):
    escaped_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{escaped_title} - Sổ điểm</title>
</head>
<body>
    <nav>
        <a href="{url_for('home')}">Trang chủ</a> | 
        <a href="{url_for('student_list')}">Sinh viên</a> | 
        <a href="{url_for('search')}">Tìm kiếm</a>
    </nav>
    <hr>
    <div>
        {body}
    </div>
</body>
</html>"""

@app.route("/")
def home():
    return layout("Trang chủ", "<p>Trang chủ</p>")

@app.route("/students")
def student_list():
    return layout("Sinh viên", "<p>Danh sách sinh viên</p>")

@app.route("/search")
def search():
    return layout("Tìm kiếm", "<p>Tìm kiếm</p>")